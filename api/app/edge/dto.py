"""HTTP data transfer objects for task endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskRequest(BaseModel):
    """Payload accepted for creating/updating a task."""

    title: str
    status: str = "todo"
    dueDate: Optional[datetime] = None


class TaskResponse(TaskRequest):
    """Response payload returned for a task."""

    id: str


class DeleteResponse(BaseModel):
    """Response payload for successful delete operations."""

    message: str
