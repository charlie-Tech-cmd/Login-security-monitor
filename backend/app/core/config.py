from pathlib import Path
from urllib.parse import quote_plus

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    app_name: str = "Login Security Monitor"
    min_password_length: int = 8
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ]

    max_failed_attempts: int = 5
    failure_window_minutes: int = 15
    lockout_minutes: int = 15

    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 15
    jwt_secret_key: str

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = ""
    postgres_db: str = "login_security_monitor"

    database_url: str | None = None

    @model_validator(mode="after")
    def assemble_database_url(self) -> "Settings":
        if not self.database_url:
            host = self.postgres_host.strip()
            # If localhost/127.0.0.1 is configured but TCP loopback is unavailable (e.g. sandboxed environment),
            # automatically connect via the active local unix socket in /tmp if present.
            if host in ("localhost", "127.0.0.1"):
                socket_file = Path(f"/tmp/.s.PGSQL.{self.postgres_port}")
                if socket_file.exists():
                    try:
                        import socket

                        with socket.create_connection(
                            (host, self.postgres_port), timeout=0.15
                        ):
                            pass
                    except (OSError, TimeoutError):
                        host = "/tmp"

            user = quote_plus(self.postgres_user)
            pwd = (
                f":{quote_plus(self.postgres_password)}"
                if self.postgres_password
                else ""
            )
            if host.startswith("/"):
                self.database_url = (
                    f"postgresql+psycopg2://{user}{pwd}@/{self.postgres_db}"
                    f"?host={host}&port={self.postgres_port}"
                )
            else:
                self.database_url = (
                    f"postgresql+psycopg2://{user}{pwd}@{host}:{self.postgres_port}/{self.postgres_db}"
                )
        return self

    model_config = SettingsConfigDict(
        env_file=(str(BACKEND_DIR / ".env"), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
