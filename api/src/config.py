"""
Single source of truth for all application configuration

Reads environment variables (and optionally a .env file) and exposes them
as typed, validated attributes. The application will fail fast at startup
if any required variable is missing or malformed - rather than at the point
of first use
"""

import os
from pathlib import Path

from dotenv import load_dotenv

_ENV_FILE = Path(__file__).parent.parent / ".env"


def _required_env(key: str) -> str:
    """
    Read a required environment variable
    Raises a ValueError if the variable is missing or empty
    """
    value = os.getenv(key)

    if value is None or value == "":
        raise ValueError(f"Missing required environment variable: {key}")
    
    return value


class Settings:
    """
    Application settings loaded from environment variables and optional .env
    """

    db_url: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    ui_origins: str

    def __init__(self) -> None:
        load_dotenv(dotenv_path=_ENV_FILE)

        connection_string = (os.getenv("DATABASE_CONNECTION_STRING") or "").strip()

        if connection_string:
            self.db_url = connection_string
            self.db_user = ""
            self.db_password = ""
            self.db_host = ""
            self.db_port = 5432
            self.db_name = ""

        else:
            self.db_user = _required_env("DB_USER")
            self.db_password = _required_env("DB_PASSWORD")
            self.db_host = _required_env("DB_HOST")
            
            db_port_value = os.getenv("DB_PORT", "5432")
            try:
                self.db_port = int(db_port_value)
            except ValueError as exc:
                raise ValueError(
                    f"DB_PORT must be an integer, got {db_port_value!r}"
                ) from exc
            
            self.db_name = _required_env("DB_NAME")
            self.db_url = (
                f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}?sslmode=prefer"
            )

        self.ui_origins = os.getenv("UI_ORIGINS", "")

    @property
    def database_url(self) -> str:
        """
        Construct the connection string
        """
        return self.db_url


try:
    settings = Settings()
except ValueError as exc:
    raise SystemExit(f"Configuration error: {exc}") from exc