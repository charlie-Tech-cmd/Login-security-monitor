from dataclasses import dataclass

from app.core.config import settings
from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.services.login_monitor import LoginMonitor
from app.services.user_store import InMemoryUserStore, UserRecord


@dataclass(frozen=True)
class AuthResult:
    success: bool
    message: str
    user: UserRecord | None = None
    access_token: str | None = None


class AuthService:
    """Handle email registration, login verification, and failed-login monitoring."""

    def __init__(
        self,
        user_store: InMemoryUserStore,
        login_monitor: LoginMonitor,
    ) -> None:
        self.user_store = user_store
        self.login_monitor = login_monitor

    def register(self, email: str, password: str) -> UserRecord:
        email = email.strip()

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")

        if len(password) > 128:
            raise ValueError("Password must not exceed 128 characters.")

        password_hash = hash_password(password)

        return self.user_store.create_user(
            email=email,
            password_hash=password_hash,
        )

    def login(self, email: str, password: str) -> AuthResult:
        email = email.strip()

        if not email:
            return AuthResult(False, "Invalid credentials.")

        if self.login_monitor.is_locked(email):
            return AuthResult(
                False,
                "Too many failed login attempts. Please try again later.",
            )

        user = self.user_store.get_by_identifier(email)

        if user is None:
            self.login_monitor.record_failure(email)
            return AuthResult(False, "Invalid credentials.")

        if not verify_password(password, user.password_hash):
            self.login_monitor.record_failure(email)
            return AuthResult(False, "Invalid credentials.")

        self.login_monitor.record_success(email)

        token = create_access_token(subject=user.id)

        return AuthResult(
            success=True,
            message="Login successful.",
            user=user,
            access_token=token,
        )


user_store = InMemoryUserStore()

login_monitor = LoginMonitor(
    max_failed_attempts=settings.max_failed_attempts,
    failure_window_minutes=settings.failure_window_minutes,
    lockout_minutes=settings.lockout_minutes,
)

auth_service = AuthService(user_store, login_monitor)
