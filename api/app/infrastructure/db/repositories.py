"""SQLAlchemy repository adapter for task persistence."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.domain.task import Task
from app.models import Task as TaskModel


class SqlAlchemyTaskRepository:
    """Repository adapter that fulfills `TaskRepositoryPort` using SQLAlchemy."""

    def __init__(self, db: Session):
        """Initialize repository with an active SQLAlchemy session."""
        self.db = db

    def list_tasks(self) -> list[Task]:
        """Fetch and map all persisted tasks to domain objects."""
        tasks = self.db.query(TaskModel).all()
        return [self._to_domain(task) for task in tasks]

    def create_task(self, title: str, status: str, due_date: Optional[datetime]) -> Task:
        """Persist a new task and return its domain representation."""
        db_task = TaskModel(id=str(uuid.uuid4()), title=title, status=status, dueDate=due_date)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return self._to_domain(db_task)

    def update_task(self, task_id: str, title: str, status: str, due_date: Optional[datetime]) -> Task | None:
        """Update an existing task and return it, or ``None`` if missing."""
        task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            return None

        task.title = title
        task.status = status
        task.dueDate = due_date
        self.db.commit()
        self.db.refresh(task)
        return self._to_domain(task)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by id and return whether a row was deleted."""
        task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            return False

        self.db.delete(task)
        self.db.commit()
        return True

    @staticmethod
    def _to_domain(task: TaskModel) -> Task:
        """Map ORM model to domain entity."""
        return Task(id=task.id, title=task.title, status=task.status, due_date=task.dueDate)
