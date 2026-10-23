import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.routes.auth import auth_service
from app.services.login_monitor import LoginMonitor
from app.services.user_store import InMemoryUserStore


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(auth_service, "user_store", InMemoryUserStore())
    monkeypatch.setattr(auth_service, "login_monitor", LoginMonitor())

    with TestClient(app) as test_client:
        yield test_client


def register_user(client, email="testuser@example.com", password="SecurePass123!"):
    return client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )


def login_user(client, email="testuser@example.com", password="SecurePass123!"):
    return client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )


def test_register_endpoint_creates_user(client):
    response = register_user(client)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data
    assert "username" not in data
    assert "role" not in data


def test_register_rejects_duplicate_email(client):
    register_user(client)

    response = register_user(client)

    assert response.status_code == 409


def test_register_rejects_invalid_email(client):
    response = register_user(client, email="not-an-email")

    assert response.status_code == 422


def test_register_rejects_password_shorter_than_eight_characters(client):
    response = register_user(client, password="abc1234")

    assert response.status_code == 422


def test_login_endpoint_returns_access_token(client):
    register_user(client)

    response = login_user(client)

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_login_rejects_wrong_password(client):
    register_user(client)

    response = login_user(client, password="WrongPassword123!")

    assert response.status_code == 401


def test_me_endpoint_returns_authenticated_user(client):
    register_user(client)
    login_response = login_user(client)

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    assert "password_hash" not in data
    assert "username" not in data
    assert "role" not in data


def test_me_endpoint_rejects_missing_token(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401


def test_me_endpoint_rejects_invalid_token(client):
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401


def test_five_failed_logins_trigger_lockout(client):
    register_user(client)

    for _ in range(5):
        response = login_user(client, password="WrongPassword123!")
        assert response.status_code == 401

    response = login_user(client)
    assert response.status_code == 401


def test_login_requires_email_and_password(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "testuser@example.com"},
    )

    assert response.status_code == 422
