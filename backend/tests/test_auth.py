import pytest

from app.core.security import (
    hash_password,
    validate_password,
    verify_password,
)


def test_password_with_eight_characters_is_accepted():
    validate_password("Campus1!")


def test_password_longer_than_eight_characters_is_accepted():
    validate_password("SecureCampus123!")


def test_password_shorter_than_eight_characters_is_rejected():
    with pytest.raises(ValueError):
        validate_password("abc123")


def test_empty_password_is_rejected():
    with pytest.raises(ValueError):
        validate_password("")


def test_password_hash_is_not_plaintext():
    password = "SecureCampus123!"
    hashed = hash_password(password)

    assert hashed != password
    assert password not in hashed


def test_correct_password_matches_hash():
    password = "SecureCampus123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_incorrect_password_does_not_match_hash():
    hashed = hash_password("SecureCampus123!")

    assert verify_password("WrongPassword123!", hashed) is False


def test_same_password_produces_different_hashes():
    password = "SecureCampus123!"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash
    assert verify_password(password, first_hash) is True
    assert verify_password(password, second_hash) is True
