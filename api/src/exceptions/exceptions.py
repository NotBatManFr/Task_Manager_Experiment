"""
Custom domain exceptions for the Task application
"""

class TaskNotFoundException(Exception):
    """
    Raised when a task with the requested ID does not exist in the database

    Attributes
    ----------
    task_id : str
        The ID that was looked up and not found
    """
    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")

class TaskDeleteError(Exception):
    """
    Raised when a task deletion operation fails at the repository layer

    Attributes
    ----------
    task_id : str
        The ID of the task that could not be deleted
    """
    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        super().__init__(f"Failed to delete task with ID {task_id} from the database")