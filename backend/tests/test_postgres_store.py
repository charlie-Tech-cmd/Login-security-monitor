import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.database import SessionLocal, engine, init_db
from app.main import app
from app.models.user import UserModel
from app.services.auth_service import auth_service
from app.services.user_store import PostgresUserStore


@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE users;"))
    yield
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE users;"))


def test_postgres_table_exists():
    with engine.connect() as conn:
        tables = conn.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        ).fetchall()
        table_names = [t[0] for t in tables]
        assert "users" in table_names


def test_postgres_user_store_create_and_retrieve():
    store = PostgresUserStore()
    user = store.create_user("alice@example.com", "argon2_test_hash_123")

    assert user.id is not None
    assert user.email == "alice@example.com"
    assert user.password_hash == "argon2_test_hash_123"

    # Case-insensitive lookup
    by_email = store.get_by_identifier("ALICE@EXAMPLE.COM")
    assert by_email is not None
    assert by_email.id == user.id

    by_id = store.get_by_id(user.id)
    assert by_id is not None
    assert by_id.email == "alice@example.com"


def test_postgres_user_store_duplicate_email_rejected():
    store = PostgresUserStore()
    store.create_user("duplicate@example.com", "hash1")

    with pytest.raises(ValueError, match="Email already registered"):
        store.create_user("duplicate@example.com", "hash2")


def test_postgres_user_store_nonexistent_returns_none():
    store = PostgresUserStore()
    assert store.get_by_identifier("doesnotexist@example.com") is None
    assert store.get_by_id("non-existent-uuid") is None


def test_postgres_e2e_register_login_me():
    # Ensure auth_service uses PostgresUserStore
    auth_service.user_store = PostgresUserStore()

    with TestClient(app) as client:
        # 1. Register through API
        reg_res = client.post(
            "/api/auth/register",
            json={"email": "pg_user@example.com", "password": "SecurePassword123!"},
        )
        assert reg_res.status_code == 201
        data = reg_res.json()
        user_id = data["id"]
        assert data["email"] == "pg_user@example.com"

        # 2. Verify directly in PostgreSQL database table
        with SessionLocal() as session:
            db_user = session.get(UserModel, user_id)
            assert db_user is not None
            assert db_user.email == "pg_user@example.com"
            assert db_user.password_hash.startswith("$argon2id$")

        # 3. Login through API
        login_res = client.post(
            "/api/auth/login",
            json={"email": "pg_user@example.com", "password": "SecurePassword123!"},
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]

        # 4. Access protected /me route
        me_res = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me_res.status_code == 200
        assert me_res.json()["email"] == "pg_user@example.com"
        assert me_res.json()["id"] == user_id

