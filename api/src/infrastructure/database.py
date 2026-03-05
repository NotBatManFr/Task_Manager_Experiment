"""
Create a SQLAlchemy engine and session factory

Exports
-------
- Base          : SQLAlchemy declarative base (imported by models.py)
- init_db()     : Called once at startup; returns (engine, SessionLocal)
"""

import logging
import time

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import QueuePool


logger = logging.getLogger(__name__)

# Maximum number of connection attempts
_MAX_RETRIES = 5
# Delay between retries in seconds
_RETRY_DELAY = 2

class Base(DeclarativeBase):
    """
    Declarative base class shared by all ORM models
    """
    pass

def build_engine(database_url: str) -> Engine:
    """    
    Create a SQLAlchemy engine with connection pooling configured for a
    long-running web service

    Pool settings
    -------------
    pool_size       : Persistent connections kept open. Set to 5 for a small
                      service; tune upward under load.
    max_overflow    : Temporary connections allowed beyond pool_size.
    pool_pre_ping   : Issue a lightweight SELECT 1 before handing out a
                      connection — catches stale connections after DB restarts.
    pool_recycle    : Force-recycle connections older than 1 hour to prevent
                      "server closed the connection unexpectedly" errors on
                      long-idle instances.
    """

    return create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=5,  # Number of connections to maintain
        max_overflow=10,  # Max connections beyond pool_size
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,  # Recycle connections after 1 hour
        echo=False,  # Set to True for SQL query logging in development
    )


def init_db(database_url: str) -> tuple[Engine, sessionmaker]:
    """
    Initialise the database engine with a startup retry loop

    Parameters
    ----------
    database_url : str
        Full SQLAlchemy connection string

    Returns
    -------
    tuple[Engine, sessionmaker]
        A configured engine and a bound session factory

    Raises
    ------
    RuntimeError
        If the database cannot be reached after _MAX_RETRIES attempts
    """
    for attempt in range(_MAX_RETRIES):
        try:
            engine = build_engine(database_url)
            
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            logger.info("Database connection established successfully")

            session_local = sessionmaker(autocommit=False, 
                                         autoflush=False, 
                                         bind=engine)
            return engine, session_local
        
        except OperationalError as exception:
            if attempt < _MAX_RETRIES - 1:
                logger.warning(
                    f"Database connection failed, retrying in {_RETRY_DELAY} seconds..."
                    f"\n(attempt {attempt + 1}/{_MAX_RETRIES})"
                    f"\n: {exception}")
                time.sleep(_RETRY_DELAY)

            else: 
                raise RuntimeError(
                    f"Database connection failed after {_MAX_RETRIES} attempts: {exception}"
                    "\nPlease check your database configuration and ensure the database is running."
                    ) from exception