"""Database setup and session management.

Supports:
- explicit `DATABASE_URL` configuration,
- fallback Postgres URL from legacy env vars,
- local SQLite fallback for development/tests when credentials are absent.
"""

import os
import time

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool

load_dotenv()


def _build_database_url() -> str:
    """Resolve database URL from environment with sensible fallbacks."""
    explicit_database_url = os.getenv("DATABASE_URL")
    if explicit_database_url:
        return explicit_database_url

    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port")
    dbname = os.getenv("dbname")

    if all([user, password, host, port, dbname]):
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}?sslmode=require"

    return "sqlite:///./task_manager.db"


DATABASE_URL = _build_database_url()


def _init_engine(database_url: str):
    """Initialize SQLAlchemy engine with retries for non-SQLite databases."""
    if database_url.startswith("sqlite"):
        return create_engine(database_url, connect_args={"check_same_thread": False})

    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            engine = create_engine(
                database_url,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False,
            )
            with engine.connect():
                print("✓ Database connection established successfully")
            return engine
        except OperationalError as error:
            if attempt < max_retries - 1:
                print(f"⚠ Database not ready yet, retrying in {retry_delay}s (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                continue

            raise Exception(
                "Could not connect to the database. "
                "Please check your DATABASE_URL and ensure the database is accessible."
            ) from error

    raise Exception("Database engine initialization failed")


engine = _init_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Yield a database session for request scope and close it afterward."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
