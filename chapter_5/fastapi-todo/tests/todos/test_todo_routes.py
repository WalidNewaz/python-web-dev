import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Define a fixture to instantiate the service
@pytest.fixture(scope="module")
def auth_token():
    """Login to get a token."""
    response = client.post("/auth/token", data={"username": "alice", "password": "wonderland"})
    assert response.status_code == 200
    token_instance = response.json()["access_token"]
    return token_instance


def test_create_todo(auth_token) -> None:
    """Test the addition of a todo item."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/todos", json={"title": "Learn FastAPI"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Learn FastAPI"
    assert data["completed"] is False

def test_list_todos(auth_token) -> None:
    """Test the list of todo items added."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/todos", headers=headers)
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) == 1
    assert todos[0]["title"] == "Learn FastAPI"
    assert todos[0]["completed"] is False

def test_get_todo(auth_token) -> None:
    """Test fetching a single todo item."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/todos/1", headers=headers)
    assert response.status_code == 200
    todo = response.json()
    assert todo["title"] == "Learn FastAPI"
    assert todo["completed"] is False

def test_update_todo(auth_token) -> None:
    """Test updating an existing todo item."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.put("/api/todos/1", json={"title": "Updated learning FastAPI"}, headers=headers)
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo["title"] == "Updated learning FastAPI"
    assert updated_todo["completed"] is False

def test_delete_todo(auth_token) -> None:
    """Tests deletion of a todo item."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete("/api/todos/1", headers=headers)
    assert response.status_code == 200
    response = client.get("/api/todos/1", headers=headers)
    assert response.status_code == 404
    response = client.get("/api/todos", headers=headers)
    data = response.json()
    assert len(data) == 0

def test_validation_error(auth_token) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/todos", json={}, headers=headers)
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "Validation failed"
    assert "details" in body
