from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from threading import Lock


MAX_FAILED_ATTEMPTS = 5
FAILURE_WINDOW_MINUTES = 15
LOCKOUT_MINUTES = 15


@dataclass
class LoginAttemptState:
    failed_attempts: list[datetime] = field(default_factory=list)
    locked_until: datetime | None = None


class LoginMonitor:
    """
    Track failed login attempts and temporarily lock accounts.

    This initial implementation uses in-memory storage for development.
    Use persistent, shared storage before deploying multiple workers
    or running this service in production.
    """

    def __init__(
        self,
        max_failed_attempts: int = MAX_FAILED_ATTEMPTS,
        failure_window_minutes: int = FAILURE_WINDOW_MINUTES,
        lockout_minutes: int = LOCKOUT_MINUTES,
    ) -> None:
        if max_failed_attempts < 1:
            raise ValueError("max_failed_attempts must be at least 1.")
        if failure_window_minutes < 1:
            raise ValueError("failure_window_minutes must be at least 1.")
        if lockout_minutes < 1:
            raise ValueError("lockout_minutes must be at least 1.")

        self.max_failed_attempts = max_failed_attempts
        self.failure_window = timedelta(minutes=failure_window_minutes)
        self.lockout_duration = timedelta(minutes=lockout_minutes)

        self._states: dict[str, LoginAttemptState] = {}
        self._lock = Lock()

    @staticmethod
    def _normalize_identifier(identifier: str) -> str:
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError("A non-empty login identifier is required.")

        return identifier.strip().casefold()

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    def is_locked(self, identifier: str) -> bool:
        """Return True if the identifier is currently locked."""
        key = self._normalize_identifier(identifier)
        now = self._now()

        with self._lock:
            state = self._states.get(key)
            if state is None or state.locked_until is None:
                return False

            if now < state.locked_until:
                return True

            # Lockout expired. Start a fresh failure-tracking period.
            state.locked_until = None
            state.failed_attempts.clear()
            return False

    def record_failure(self, identifier: str) -> int:
        """
        Record a failed login and return the failures in the active window.

        Once the threshold is reached, the identifier is locked.
        Attempts made during an active lockout do not extend it.
        """
        key = self._normalize_identifier(identifier)
        now = self._now()

        with self._lock:
            state = self._states.setdefault(key, LoginAttemptState())

            if state.locked_until is not None and now < state.locked_until:
                return len(state.failed_attempts)

            if state.locked_until is not None and now >= state.locked_until:
                state.locked_until = None
                state.failed_attempts.clear()

            cutoff = now - self.failure_window
            state.failed_attempts = [
                attempt
                for attempt in state.failed_attempts
                if attempt > cutoff
            ]

            state.failed_attempts.append(now)

            if len(state.failed_attempts) >= self.max_failed_attempts:
                state.locked_until = now + self.lockout_duration

            return len(state.failed_attempts)

    def record_success(self, identifier: str) -> None:
        """Clear failure tracking after a successful login."""
        key = self._normalize_identifier(identifier)

        with self._lock:
            self._states.pop(key, None)

    def remaining_lockout_seconds(self, identifier: str) -> int:
        """Return remaining lockout seconds, or zero if not locked."""
        key = self._normalize_identifier(identifier)
        now = self._now()

        with self._lock:
            state = self._states.get(key)
            if state is None or state.locked_until is None:
                return 0

            remaining = (state.locked_until - now).total_seconds()
            if remaining <= 0:
                state.locked_until = None
                state.failed_attempts.clear()
                return 0

            return int(remaining) + 1


login_monitor = LoginMonitor()
