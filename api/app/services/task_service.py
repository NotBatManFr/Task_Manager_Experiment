"""
Business logic layer for Task operations
"""

import uuid

from app.exceptions import TaskNotFoundException, TaskDeleteError
from app.models import Task
from app.repository import TaskRepository
from app.schema.task_create import TaskCreate
from app.schema.task_update import TaskUpdate

class TaskServices:
    """
    Orchestrates business logic for Task operations
    """
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieves all tasks as List[Task] from the repository
        """
        return self.repository.get_all()

    def create_task(self, task_data: TaskCreate) -> Task:
        """
        Creates the new task from the payload with a unique ID

        Parameters:
        - task_data: TaskCreate schema containing the title, status, and due date for the new task
        Returns:
        - The created Task instance with the generated ID
        """
        task = Task(
            id=str(uuid.uuid4()),
            title=task_data.title,
            status=task_data.status,
            due_date=task_data.due_date
        )
        return self.repository.add(task)

    def update_task(self, task_id: str, task_data: TaskUpdate) -> Task | None:
        """
        Fully replace the fields of an existing task (PUT semantics)

        Parameters
        ----------
        task_id : str
            The UUID of the task to update
        task_data : TaskUpdate
            Validated inbound request data containing the replacement values

        Returns
        -------
        Task
            The updated task as persisted

        Raises
        ------
        TaskNotFoundError
            If no task with the given ID exists
        """
        task = self.repository.get_by_id(task_id)
        
        if task is None:
            raise TaskNotFoundException(task_id)
        
        task.title = task_data.title
        task.status = task_data.status
        task.due_date = task_data.due_date

        return self.repository.update(task)
    
    def delete_task(self, task_id: str) -> None:
        """
        Remove a task from the data store

        Parameters
        ----------
        task_id : str
            The UUID of the task to delete

        Raises
        ------
        TaskNotFoundError
            If no task with the given ID exists
        """
        task = self.repository.get_by_id(task_id)
        
        if task is None:
            raise TaskNotFoundException(task_id)
        
        if not self.repository.remove(task):
            raise TaskDeleteError(task_id)