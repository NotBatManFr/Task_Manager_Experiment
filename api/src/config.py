"""
Single source of truth for all application configuration

Reads environment variables (and optionally a .env file) and exposes them
as typed, validated attributes. The application will fail fast at startup
if any required variable is missing or malformed - rather than at the point
of first use
"""

import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

_ENV_FILE = Path(__file__).parent.parent / ".env"


def _env(key: str, default: str = "", *, required: bool = False) -> str:
    """
    Read and trim an environment variable.
    """
    value = (os.getenv(key) or default).strip()
    if required and value == "":
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
    ui_origins_list: list[str]

    def __init__(self) -> None:
        if _ENV_FILE.exists():
            load_dotenv(dotenv_path=_ENV_FILE, override=False)

        connection_string = _env("DB_URL")

        if connection_string:
            self.db_url = connection_string
            self.db_user = ""
            self.db_password = ""
            self.db_host = ""
            self.db_port = 5432
            self.db_name = ""

        else:
            self.db_user = _env("DB_USER", required=True)
            self.db_password = _env("DB_PASSWORD", required=True)
            self.db_host = _env("DB_HOST", required=True)
            self.db_name = _env("DB_NAME", required=True)
            db_port_value = _env("DB_PORT", "5432", required=True)
            db_sslmode = _env("DB_SSLMODE", "prefer")

            try:
                self.db_port = int(db_port_value)
            except ValueError as exc:
                raise ValueError(f"DB_PORT must be an integer, got {db_port_value!r}") from exc

            # Encode credentials in case they include special URL characters.
            encoded_user = quote_plus(self.db_user)
            encoded_password = quote_plus(self.db_password)

            self.db_url = (
                f"postgresql+psycopg2://{encoded_user}:{encoded_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}?sslmode={db_sslmode}"
            )

        self.ui_origins = _env("UI_ORIGINS")
        self.ui_origins_list = [origin.strip() for origin in self.ui_origins.split(",") if origin.strip()]

    @property
    def database_url(self) -> str:
        """
        Construct the connection string
        """
        return self.db_url

    @property
    def cors_origins(self) -> list[str]:
        """
        Return parsed CORS origins as a typed list.
        """
        return self.ui_origins_list


try:
    settings = Settings()
except ValueError as exc:
    raise SystemExit(f"Configuration error: {exc}") from exc