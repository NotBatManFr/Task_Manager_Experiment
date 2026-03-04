"""Task HTTP routes.

Exposes both unversioned (`/tasks`) and versioned (`/v1/tasks`) endpoints to
maintain backward compatibility while enabling API evolution.
"""

from app.domain.task import Task
from fastapi import APIRouter, Depends, HTTPException

from app.application.task_service import TaskService
from app.bootstrap.container import get_task_service
from app.edge.dto import DeleteResponse, TaskRequest, TaskResponse

router = APIRouter(tags=["tasks"])


def _to_response(task: Task) -> TaskResponse:
    """Map a domain `Task` to the outward-facing HTTP response DTO."""
    return TaskResponse(id=task.id, title=task.title, status=task.status, dueDate=task.due_date)


@router.post("/tasks", response_model=TaskResponse)
@router.post("/v1/tasks", response_model=TaskResponse)
def create_task(task_data: TaskRequest, service: TaskService = Depends(get_task_service)):
    """Create a task from the provided request payload."""
    task = service.create_task(title=task_data.title, status=task_data.status, due_date=task_data.dueDate)
    return _to_response(task)


@router.get("/tasks", response_model=list[TaskResponse])
@router.get("/v1/tasks", response_model=list[TaskResponse])
def get_tasks(service: TaskService = Depends(get_task_service)):
    """List all tasks."""
    tasks = service.list_tasks()
    return [_to_response(task) for task in tasks]


@router.put("/tasks/{task_id}", response_model=TaskResponse)
@router.put("/v1/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_data: TaskRequest, service: TaskService = Depends(get_task_service)):
    """Update task fields for a given task id."""
    task = service.update_task(task_id=task_id, title=task_data.title, status=task_data.status, due_date=task_data.dueDate)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return _to_response(task)


@router.delete("/tasks/{task_id}", response_model=DeleteResponse)
@router.delete("/v1/tasks/{task_id}", response_model=DeleteResponse)
def delete_task(task_id: str, service: TaskService = Depends(get_task_service)):
    """Delete a task by id."""
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return DeleteResponse(message="Task deleted successfully")
