"""Application service for task use-cases.

`TaskService` orchestrates operations over the repository port and keeps edge
handlers free from persistence details.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.application.ports import TaskRepositoryPort
from app.domain.task import Task


class TaskService:
    """Use-case service for task CRUD operations."""

    def __init__(self, repository: TaskRepositoryPort):
        """Initialize service with a repository implementation."""
        self.repository = repository

    def list_tasks(self) -> list[Task]:
        """List all tasks."""
        return self.repository.list_tasks()

    def create_task(self, title: str, status: str, due_date: Optional[datetime]) -> Task:
        """Create a new task."""
        return self.repository.create_task(title=title, status=status, due_date=due_date)

    def update_task(self, task_id: str, title: str, status: str, due_date: Optional[datetime]) -> Task | None:
        """Update an existing task by id."""
        return self.repository.update_task(task_id=task_id, title=title, status=status, due_date=due_date)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by id."""
        return self.repository.delete_task(task_id)
