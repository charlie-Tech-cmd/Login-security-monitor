from dataclasses import dataclass
from threading import Lock
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import SessionLocal
from app.models.user import UserModel


@dataclass(frozen=True)
class UserRecord:
    id: str
    email: str
    password_hash: str


class PostgresUserStore:
    """
    PostgreSQL-backed user storage using SQLAlchemy.
    Stores and retrieves persistent user records.
    """

    def __init__(
        self,
        session_factory: sessionmaker[Session] = SessionLocal,
    ) -> None:
        self._session_factory = session_factory

    @staticmethod
    def _normalize(email: str) -> str:
        return email.strip().casefold()

    def create_user(self, email: str, password_hash: str) -> UserRecord:
        normalized_email = self._normalize(email)
        user_id = str(uuid4())

        with self._session_factory() as session:
            stmt = select(UserModel).where(
                func.lower(UserModel.email) == normalized_email
            )
            existing = session.scalar(stmt)
            if existing is not None:
                raise ValueError("Email already registered.")

            user_model = UserModel(
                id=user_id,
                email=email.strip(),
                password_hash=password_hash,
            )
            session.add(user_model)
            try:
                session.commit()
                session.refresh(user_model)
            except IntegrityError as exc:
                session.rollback()
                raise ValueError("Email already registered.") from exc

            return UserRecord(
                id=user_model.id,
                email=user_model.email,
                password_hash=user_model.password_hash,
            )

    def get_by_identifier(self, email: str) -> UserRecord | None:
        normalized_email = self._normalize(email)

        with self._session_factory() as session:
            stmt = select(UserModel).where(
                func.lower(UserModel.email) == normalized_email
            )
            user_model = session.scalar(stmt)
            if user_model is None:
                return None

            return UserRecord(
                id=user_model.id,
                email=user_model.email,
                password_hash=user_model.password_hash,
            )

    def get_by_id(self, user_id: str) -> UserRecord | None:
        with self._session_factory() as session:
            stmt = select(UserModel).where(UserModel.id == user_id)
            user_model = session.scalar(stmt)
            if user_model is None:
                return None

            return UserRecord(
                id=user_model.id,
                email=user_model.email,
                password_hash=user_model.password_hash,
            )


class InMemoryUserStore:
    """
    Development and isolated test fallback user store.
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
