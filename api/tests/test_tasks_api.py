"""Integration-style API tests for task endpoints."""


def test_health_endpoint(client):
    """Health endpoint should return healthy status metadata."""
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"


def test_tasks_crud_flow_unversioned(client):
    """Unversioned routes should support end-to-end create/read/update/delete."""
    create_response = client.post(
        "/tasks",
        json={"title": "Test task", "status": "todo", "dueDate": None},
    )
    assert create_response.status_code == 200

    created_task = create_response.json()
    task_id = created_task["id"]
    assert created_task["title"] == "Test task"

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    list_payload = list_response.json()
    assert len(list_payload) == 1
    assert list_payload[0]["id"] == task_id

    update_response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated task", "status": "in_progress", "dueDate": None},
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated task"

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted successfully"


def test_versioned_routes_work(client):
    """Versioned routes should be functionally equivalent to unversioned routes."""
    create_response = client.post(
        "/v1/tasks",
        json={"title": "Versioned task", "status": "todo", "dueDate": None},
    )
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    list_response = client.get("/v1/tasks")
    assert list_response.status_code == 200
    assert any(task["id"] == task_id for task in list_response.json())


def test_update_returns_404_for_missing_task(client):
    """Updating unknown task should return 404 with clear error detail."""
    response = client.put(
        "/tasks/missing-id",
        json={"title": "Nope", "status": "todo", "dueDate": None},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_returns_404_for_missing_task(client):
    """Deleting unknown task should return 404 with clear error detail."""
    response = client.delete("/tasks/missing-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
