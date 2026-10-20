from dataclasses import dataclass
from threading import Lock
from uuid import uuid4


@dataclass(frozen=True)
class UserRecord:
    id: str
    email: str
    password_hash: str


class InMemoryUserStore:
    """
    Development-only user store.
    Replace with a persistent database adapter before deployment.
    """

    def __init__(self) -> None:
        self._users_by_id: dict[str, UserRecord] = {}
        self._id_by_email: dict[str, str] = {}
        self._lock = Lock()

    @staticmethod
    def _normalize(email: str) -> str:
        return email.strip().casefold()

    def create_user(self, email: str, password_hash: str) -> UserRecord:
        normalized_email = self._normalize(email)

        with self._lock:
            if normalized_email in self._id_by_email:
                raise ValueError("Email already registered.")

            user = UserRecord(
                id=str(uuid4()),
                email=email.strip(),
                password_hash=password_hash,
            )

            self._users_by_id[user.id] = user
            self._id_by_email[normalized_email] = user.id

            return user

    def get_by_identifier(self, email: str) -> UserRecord | None:
        normalized_email = self._normalize(email)

        with self._lock:
            user_id = self._id_by_email.get(normalized_email)
            if user_id is None:
                return None

            return self._users_by_id.get(user_id)

    def get_by_id(self, user_id: str) -> UserRecord | None:
        with self._lock:
            return self._users_by_id.get(user_id)
