"""Dependency-injection container helpers.

This module wires framework dependencies to application services.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.task_service import TaskService
from app.database import get_db
from app.infrastructure.db.repositories import SqlAlchemyTaskRepository


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Build and return a `TaskService` using the SQLAlchemy repository adapter."""
    repository = SqlAlchemyTaskRepository(db)
    return TaskService(repository)
