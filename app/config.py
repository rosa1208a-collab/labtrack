from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./data/labtrack.db"
    allowed_origins: list[str] = ["http://127.0.0.1:8010", "http://localhost:8010"]
    session_cookie_secure: bool = False
    session_hours: int = Field(default=8, ge=1, le=48)
    demo_password: str | None = None
