from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings read from environment variables or backend/.env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./campus_sports_booking.db"
    cors_origins: list[str] = ["http://localhost:5173"]

    # in .env se pune un secret adevarat, valoarea de aici e doar pentru dezvoltare
    jwt_secret: str = "dev-secret-doar-pentru-dezvoltare-locala"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60


@lru_cache
def get_settings() -> Settings:
    return Settings()
