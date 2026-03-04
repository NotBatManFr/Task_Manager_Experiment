# Pydantic models that validate data to be fetched by the API.

from pydantic import BaseModel, ConfigDict, Field

from datetime import datetime
from typing import Optional

class TaskResponse (BaseModel):
    """
    Represents a Task returned by the API.

    Fields:
    - id: The unique identifier of the task.
    - title: The title of the task.
    - status: The status of the task.
    - duedate: The due date for the task.
    """
    
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="task id")
    title: str = Field(description="task title")
    status: str = Field(description="task status")
    duedate: Optional[datetime] = Field(default=None, description="task due date")