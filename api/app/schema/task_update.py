# Pydantic models that validate data to be updated in the API.

from pydantic import BaseModel, Field

from datetime import datetime
from typing import Optional

class TaskUpdate(BaseModel):
    """
    Payload for updating an existing task.
    
    Fields:
    - title: The title of the task.
    - status: The status of the task.
    - duedate: The due date for the task.
    """

    title: str = Field(..., description="task title")
    status: str = Field(..., description="task status")
    due_date: Optional[datetime] = Field(default=None, description="task due date")