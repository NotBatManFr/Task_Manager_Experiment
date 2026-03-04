"""Application-layer ports for task persistence.

This module defines protocol contracts that infrastructure adapters must implement.
It keeps the application layer decoupled from concrete ORM/database details.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Protocol

from app.domain.task import Task


class TaskRepositoryPort(Protocol):
    """Contract for task repository operations used by use-cases."""

    def list_tasks(self) -> list[Task]:
        """Return all tasks."""

    def create_task(self, title: str, status: str, due_date: Optional[datetime]) -> Task:
        """Create and persist a task, returning the persisted domain object."""

    def update_task(self, task_id: str, title: str, status: str, due_date: Optional[datetime]) -> Task | None:
        """Update an existing task or return ``None`` when it does not exist."""

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by id and return whether a record was deleted."""
