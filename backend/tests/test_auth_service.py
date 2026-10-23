import pytest

from app.core.jwt import decode_access_token
from app.services.auth_service import AuthService
from app.services.login_monitor import LoginMonitor
from app.services.user_store import InMemoryUserStore


@pytest.fixture
def service():
    return AuthService(
        user_store=InMemoryUserStore(),
        login_monitor=LoginMonitor(),
    )


def test_register_creates_user_with_hashed_password(service):
    user = service.register(
        email="alice@example.com",
        password="SecurePass123!",
    )

    assert user.email == "alice@example.com"
    assert user.password_hash != "SecurePass123!"
    assert "SecurePass123!" not in user.password_hash


def test_successful_login_returns_valid_access_token(service):
    user = service.register(
        email="alice@example.com",
        password="SecurePass123!",
    )

    result = service.login("alice@example.com", "SecurePass123!")

    assert result.success is True
    assert result.user is not None
    assert result.user.id == user.id
    assert result.access_token is not None

    payload = decode_access_token(result.access_token)

    assert payload is not None
    assert payload["sub"] == user.id
    assert "role" not in payload


def test_email_login_is_case_insensitive(service):
    service.register(
        email="alice@example.com",
        password="SecurePass123!",
    )

    result = service.login("ALICE@EXAMPLE.COM", "SecurePass123!")

    assert result.success is True


def test_wrong_password_is_rejected(service):
    service.register(
        email="alice@example.com",
        password="SecurePass123!",
    )

    result = service.login("alice@example.com", "WrongPass123!")

    assert result.success is False
    assert result.access_token is None
    assert result.message == "Invalid credentials."


def test_unknown_email_is_rejected(service):
    result = service.login("unknown@example.com", "SomePassword123!")

    assert result.success is False
    assert result.access_token is None
    assert result.message == "Invalid credentials."


def test_five_failed_logins_trigger_lockout(service):
    service.register(
        email="alice@example.com",
        password="SecurePass123!",
    )

    for _ in range(5):
        service.login("alice@example.com", "WrongPass123!")

    result = service.login("alice@example.com", "SecurePass123!")

    assert result.success is False
    assert result.access_token is None
    assert "Too many failed" in result.message


def test_successful_login_clears_failed_attempts(service):
    service.register(
        email="alice@example.com",
        password="SecurePass123!",
    )

    service.login("alice@example.com", "WrongPass123!")
    service.login("alice@example.com", "WrongPass123!")

    assert service.login_monitor.remaining_lockout_seconds(
        "alice@example.com"
    ) == 0

    result = service.login("alice@example.com", "SecurePass123!")

    assert result.success is True
    assert service.login_monitor.remaining_lockout_seconds(
        "alice@example.com"
    ) == 0


def test_duplicate_email_is_rejected(service):
    service.register(
        email="alice@example.com",
        password="SecurePass123!",
    )

    with pytest.raises(ValueError, match="Email already registered"):
        service.register(
            email="ALICE@example.com",
            password="AnotherPass123!",
        )


def test_short_password_is_rejected(service):
    with pytest.raises(ValueError, match="at least 8 characters"):
        service.register(
            email="alice@example.com",
            password="short",
        )


def test_password_over_maximum_length_is_rejected(service):
    with pytest.raises(ValueError, match="must not exceed 128"):
        service.register(
            email="alice@example.com",
            password="A" * 129,
        )
