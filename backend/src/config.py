"""
Application configuration using Pydantic BaseSettings.
Handles environment variables and application settings.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database settings
    database_url: str = Field(
        default="sqlite:///./otaku_shelf.db",
        description="Database URL for SQLModel/SQLAlchemy",
    )

    # SuperTokens settings
    supertokens_connection_uri: str = Field(
        default="http://localhost:3567", description="SuperTokens core connection URI"
    )
    supertokens_api_key: str = Field(
        default="someApiKey123123123123", description="SuperTokens API key"
    )

    # Application settings
    app_name: str = Field(default="OtakuShelf", description="Application name")
    api_domain: str = Field(
        default="http://localhost:8000", description="API domain for SuperTokens"
    )
    website_domain: str = Field(
        default="http://localhost:3000",
        description="Frontend domain for CORS and SuperTokens",
    )

    # Security settings
    environment: Literal["development", "staging", "production"] = Field(
        default="development", description="Application environment"
    )

    # CORS settings
    cors_origins: list[str] = Field(
        default=["http://127.0.0.1:3000", "http://localhost:3000"],
        description="Allowed CORS origins",
    )

    # logging settings
    log_level: Literal["debug", "info", "warning", "error", "critical"] = Field(
        default="info", description="Logging level"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
