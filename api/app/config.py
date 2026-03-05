"""
Single source of truth for all application configuration

Reads environment variables (and optionally a .env file) and exposes them
as typed, validated attributes. The application will fail fast at startup
if any required variable is missing or malformed — rather than at the point
of first use
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Pydantic-settings automatically reads from environment variables
    (case-insensitive) and from an optional .env file. A missing required
    field raises a ValidationError at import time.
    """

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        populate_by_name=True
    )

    #----Database----------------

    db_user: str = Field(description="PostgreSQL Username")
    db_password: str = Field(description="PostgreSQL Password")
    db_host: str = Field(description="Database Host")
    db_port: int = Field(default=5432, description="Port Number")
    db_name: str = Field(description="Database Name")

    #----CORS---------------

    ui_origins: str = Field(
        default="",
        description="CSV of allowed CORS Origins"
    )

    #----Properties----------

    @property
    def database_url(self) -> str:
        """Construct the connection string"""
        return(
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}?sslmode=require"
        )

settings = Settings() # type: ignore[call-arg]