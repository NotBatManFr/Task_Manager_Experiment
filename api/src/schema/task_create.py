"""
Pydantic models that validate data to be created in the API.
"""

from pydantic import BaseModel, Field, AliasChoices

from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    """
    Payload for creating a new task.

    Fields:
    - title: The title of the task (required).
    - status: The status of the task (optional, defaults to "todo").
    - due_date: The due date for the task (optional).
    """

    title: str = Field(..., description="task title")
    status: str = Field(default="todo", description="task status")
    due_date: Optional[datetime] = Field(
        default=None,
        description="task due date",
        validation_alias=AliasChoices("due_date", "dueDate"),
        serialization_alias="dueDate"
    )