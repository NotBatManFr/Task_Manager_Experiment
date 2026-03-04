"""Unit tests for application task service behavior."""

from app.application.task_service import TaskService
from app.domain.task import Task


class FakeTaskRepository:
    """In-memory fake repository for `TaskService` unit tests."""

    def __init__(self):
        self.tasks = {}

    def list_tasks(self):
        """Return all fake tasks."""
        return list(self.tasks.values())

    def create_task(self, title, status, due_date):
        """Create and store a fake task."""
        task = Task(id="1", title=title, status=status, due_date=due_date)
        self.tasks[task.id] = task
        return task

    def update_task(self, task_id, title, status, due_date):
        """Update an existing fake task if present."""
        if task_id not in self.tasks:
            return None
        task = Task(id=task_id, title=title, status=status, due_date=due_date)
        self.tasks[task_id] = task
        return task

    def delete_task(self, task_id):
        """Delete fake task by id and return success flag."""
        return self.tasks.pop(task_id, None) is not None


def test_task_service_calls_repository_contract():
    """Validate that TaskService delegates CRUD semantics to repository contract."""
    repository = FakeTaskRepository()
    service = TaskService(repository)

    created = service.create_task("Service task", "todo", None)
    assert created.id == "1"

    tasks = service.list_tasks()
    assert len(tasks) == 1

    updated = service.update_task("1", "Updated service task", "done", None)
    assert updated is not None
    assert updated.status == "done"

    deleted = service.delete_task("1")
    assert deleted is True
