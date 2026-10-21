from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Login Security Monitor"
    min_password_length: int = 8
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    max_failed_attempts: int = 5
    failure_window_minutes: int = 15
    lockout_minutes: int = 15

    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 15
    jwt_secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
