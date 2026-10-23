from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT for a user identified by a stable ID."""
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("Token subject must be a non-empty string.")

    now = datetime.now(timezone.utc)
    lifetime = expires_delta or timedelta(
        minutes=settings.jwt_expiration_minutes
    )

    if lifetime.total_seconds() <= 0:
        raise ValueError("Token lifetime must be positive.")

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + lifetime,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Validate a signed JWT and return its claims, or None if invalid."""
    if not isinstance(token, str) or not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["sub", "exp", "iat"]},
        )
    except (InvalidTokenError, TypeError, ValueError):
        return None

    subject = payload.get("sub")

    if not isinstance(subject, str) or not subject.strip():
        return None

    return payload
