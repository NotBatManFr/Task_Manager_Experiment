"""
Manages application startup and shutdown lifecycle
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.infrastructure.database import Base, init_db

logger: logging.Logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup
    -------
    1. Connect to the database with retry logic
    2. Store the engine and session factory on app.state so that the
       get_db() dependency can access them without a global variable
    3. Create any missing tables (idempotent — safe to run on every start)

    Shutdown
    --------
    Dispose the engine to cleanly close all pooled connections
    """

    logger.info("Starting tasks APIs...")

    engine, session_local = init_db(settings.database_url)
    app.state.engine = engine
    app.state.session_local = session_local

    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created or verified successfully")

    yield

    logger.info("Shutting down tasks APIs...")
    engine.dispose()