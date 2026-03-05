"""
Centralised FastAPI dependency injection callables
"""

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from src.repositories.repository import TaskRepository
from src.services.task_service import TaskServices

def get_db(request: Request) -> Session:
    """
    Yield a SQLAlchemy Session for the duration of a single request.
    """
    SessionLocal = request.app.state.SessionLocal
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_task_service(db: Session = Depends(get_db)) -> TaskServices:
    """
    Factory function to create a TaskServices instance with the required dependencies
    """
    repository = TaskRepository(db)
    return TaskServices(repository)