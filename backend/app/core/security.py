from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)

# Argon2id is the default Argon2 variant used by PasswordHasher.
password_hasher = PasswordHasher()


MIN_PASSWORD_LENGTH = 8


def validate_password(password: str) -> None:
    """
    Validate the minimum password length.

    Raises:
        ValueError: If the password contains fewer than 8 characters.
    """
    if not isinstance(password, str):
        raise ValueError("Password must be a string.")

    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(
            f"Password must contain at least {MIN_PASSWORD_LENGTH} characters."
        )


def hash_password(password: str) -> str:
    """
    Validate and securely hash a password using Argon2id.
    """
    validate_password(password)

    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a submitted password against its stored hash.

    Returns False when the password does not match or the stored
    hash is invalid.
    """
    if not isinstance(plain_password, str):
        return False

    if not isinstance(hashed_password, str):
        return False

    try:
        return password_hasher.verify(
            hashed_password,
            plain_password,
        )
    except (
        VerifyMismatchError,
        VerificationError,
        InvalidHashError,
        HashingError,
    ):
        return False