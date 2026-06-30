"""
Tests for Tasks CRUD API endpoints.

Covers the /api/tasks routes added to fix the broken My Tasks feature
(App.vue was calling endpoints that didn't exist on the server).
"""
import pytest
import sys
from pathlib import Path

server_path = Path(__file__).parent.parent.parent / "server"
sys.path.insert(0, str(server_path))

import main as server_module


@pytest.fixture(autouse=True)
def clear_tasks():
    """Reset in-memory task state before each test."""
    server_module._tasks.clear()
    server_module._task_counter[0] = 0
    yield
    server_module._tasks.clear()
    server_module._task_counter[0] = 0


class TestGetTasks:
    def test_returns_200(self, client):
        response = client.get("/api/tasks")
        assert response.status_code == 200

    def test_returns_empty_list_initially(self, client):
        data = client.get("/api/tasks").json()
        assert data == []

    def test_returns_list_type(self, client):
        assert isinstance(client.get("/api/tasks").json(), list)

    def test_returns_created_tasks(self, client):
        client.post("/api/tasks", json={"title": "Task A"})
        client.post("/api/tasks", json={"title": "Task B"})
        data = client.get("/api/tasks").json()
        assert len(data) == 2


class TestCreateTask:
    def test_returns_201_or_200(self, client):
        response = client.post("/api/tasks", json={"title": "New task"})
        assert response.status_code in (200, 201)

    def test_response_contains_required_fields(self, client):
        task = client.post("/api/tasks", json={"title": "Test task"}).json()
        assert "id" in task
        assert "title" in task
        assert "priority" in task
        assert "status" in task

    def test_title_is_preserved(self, client):
        task = client.post("/api/tasks", json={"title": "Buy milk"}).json()
        assert task["title"] == "Buy milk"

    def test_default_status_is_pending(self, client):
        task = client.post("/api/tasks", json={"title": "Task"}).json()
        assert task["status"] == "pending"

    def test_default_priority_is_medium(self, client):
        task = client.post("/api/tasks", json={"title": "Task"}).json()
        assert task["priority"] == "medium"

    def test_custom_priority_is_stored(self, client):
        task = client.post("/api/tasks", json={"title": "Urgent", "priority": "high"}).json()
        assert task["priority"] == "high"

    def test_due_date_is_stored(self, client):
        task = client.post("/api/tasks", json={"title": "Task", "due_date": "2026-07-01"}).json()
        assert task["due_date"] == "2026-07-01"

    def test_ids_are_unique(self, client):
        t1 = client.post("/api/tasks", json={"title": "A"}).json()
        t2 = client.post("/api/tasks", json={"title": "B"}).json()
        assert t1["id"] != t2["id"]

    def test_missing_title_returns_422(self, client):
        response = client.post("/api/tasks", json={"priority": "high"})
        assert response.status_code == 422


class TestDeleteTask:
    def test_delete_existing_task_returns_200(self, client):
        task = client.post("/api/tasks", json={"title": "To delete"}).json()
        response = client.delete(f"/api/tasks/{task['id']}")
        assert response.status_code == 200

    def test_deleted_task_no_longer_in_list(self, client):
        task = client.post("/api/tasks", json={"title": "To delete"}).json()
        client.delete(f"/api/tasks/{task['id']}")
        ids = [t["id"] for t in client.get("/api/tasks").json()]
        assert task["id"] not in ids

    def test_delete_nonexistent_task_returns_404(self, client):
        response = client.delete("/api/tasks/does-not-exist")
        assert response.status_code == 404

    def test_other_tasks_unaffected_after_delete(self, client):
        t1 = client.post("/api/tasks", json={"title": "Keep"}).json()
        t2 = client.post("/api/tasks", json={"title": "Delete"}).json()
        client.delete(f"/api/tasks/{t2['id']}")
        remaining = client.get("/api/tasks").json()
        assert len(remaining) == 1
        assert remaining[0]["id"] == t1["id"]


class TestToggleTask:
    def test_toggle_pending_to_completed(self, client):
        task = client.post("/api/tasks", json={"title": "Toggle me"}).json()
        assert task["status"] == "pending"
        toggled = client.patch(f"/api/tasks/{task['id']}").json()
        assert toggled["status"] == "completed"

    def test_toggle_completed_back_to_pending(self, client):
        task = client.post("/api/tasks", json={"title": "Toggle twice"}).json()
        client.patch(f"/api/tasks/{task['id']}")
        toggled_back = client.patch(f"/api/tasks/{task['id']}").json()
        assert toggled_back["status"] == "pending"

    def test_toggle_returns_updated_task(self, client):
        task = client.post("/api/tasks", json={"title": "Check response"}).json()
        response = client.patch(f"/api/tasks/{task['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task["id"]
        assert data["title"] == task["title"]

    def test_toggle_nonexistent_task_returns_404(self, client):
        response = client.patch("/api/tasks/no-such-task")
        assert response.status_code == 404

    def test_status_change_persists_in_list(self, client):
        task = client.post("/api/tasks", json={"title": "Persist check"}).json()
        client.patch(f"/api/tasks/{task['id']}")
        tasks = client.get("/api/tasks").json()
        stored = next(t for t in tasks if t["id"] == task["id"])
        assert stored["status"] == "completed"
