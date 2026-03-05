"""
HTTP route definitions for the /tasks resource
"""

from fastapi import APIRouter, Depends, status, HTTPException

from src.dependencies import get_task_service
from src.services.task_service import TaskServices
from src.schema.task_create import TaskCreate
from src.schema.task_update import TaskUpdate
from src.schema.task_response import TaskResponse

router: APIRouter = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get(
    "/", 
    response_model=list[TaskResponse], 
    status_code=status.HTTP_200_OK, 
    summary="Retrieve all tasks")
def get_tasks(service: TaskServices = Depends(get_task_service)) -> list[TaskResponse]:
    """
    Retrieve a list of all tasks in the system
    """
    return service.get_all_tasks()

@router.post(
    "/", 
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task")
def create_task(task_data: TaskCreate, service: TaskServices = Depends(get_task_service)) -> TaskResponse:
    """
    Create a new task with the provided data
    """
    return service.create_task(task_data)

@router.put("/{task_id}", 
            response_model=TaskResponse, 
            status_code=status.HTTP_200_OK, 
            summary="Update an existing task")
def update_task(task_id: str, task_data: TaskUpdate, service: TaskServices = Depends(get_task_service)) -> TaskResponse:
    """
    Update an existing task with the provided data

    Parameters
    ----------
    task_id : str
        The UUID of the task to update
    task_data : TaskUpdate
        Validated inbound request data containing the replacement values

    Returns
    -------
    TaskResponse
        The updated task as persisted

    Raises
    ------
    HTTPException 404
        If no task with the given ID exists
    """
    return service.update_task(task_id, task_data)
 
    
@router.delete("/{task_id}", 
               status_code=status.HTTP_204_NO_CONTENT, 
               summary="Delete an existing task")
def delete_task(task_id: str, service: TaskServices = Depends(get_task_service)) -> None:
    """
    Delete a task by ID.

    Returns HTTP 204 No Content on success (no body).
    Returns HTTP 404 if the task does not exist.
    """
    service.delete_task(task_id)