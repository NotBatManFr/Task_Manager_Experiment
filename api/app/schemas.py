from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    status: str = "pending"

class TaskResponse(TaskCreate):
    id: str

    class Config:
        from_attributes = True