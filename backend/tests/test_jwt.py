from datetime import timedelta
import time

from app.core.jwt import create_access_token, decode_access_token


def test_valid_token_can_be_decoded():
    token = create_access_token(subject="user-123")
    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "user-123"
    assert "exp" in payload
    assert "iat" in payload
    assert "role" not in payload


def test_invalid_token_is_rejected():
    assert decode_access_token("not-a-valid-token") is None


def test_empty_token_is_rejected():
    assert decode_access_token("") is None


def test_expired_token_is_rejected():
    token = create_access_token(
        subject="user-123",
        expires_delta=timedelta(seconds=1),
    )

    time.sleep(1.1)

    assert decode_access_token(token) is None


def test_token_with_modified_signature_is_rejected():
    token = create_access_token(subject="user-123")

    header, payload, signature = token.split(".")
    modified_signature = (
        ("A" if signature[0] != "A" else "B") + signature[1:]
    )

    assert decode_access_token(
        f"{header}.{payload}.{modified_signature}"
    ) is None


def test_empty_subject_is_rejected():
    import pytest

    with pytest.raises(ValueError):
        create_access_token(subject=" ")
