from fastapi.testclient import TestClient
from fastapi_todo.main import app
import json

client = TestClient(app)

def test_read_root() -> None:
    """Test that the root endpoint returns the correct JSON response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}

def test_create_todo() -> None:
    """Test the addition of a todo item."""
    response = client.post("/todos", json={"title": "Learn FastAPI"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Learn FastAPI"
    assert data["completed"] is False

def test_list_todos() -> None:
    """Test the list of todo items added."""
    response = client.get("/todos")
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) == 1
    assert todos[0]["title"] == "Learn FastAPI"
    assert todos[0]["completed"] is False

def test_get_todo() -> None:
    """Test fetching a single todo item."""
    response = client.get("/todos/1")
    assert response.status_code == 200
    todo = response.json()
    assert todo["title"] == "Learn FastAPI"
    assert todo["completed"] is False

def test_update_todo() -> None:
    """Test updating an existing todo item."""
    response = client.put("/todos/1", json={"title": "Updated learning FastAPI"})
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo["title"] == "Updated learning FastAPI"
    assert updated_todo["completed"] is False

def test_delete_todo() -> None:
    """Tests deletion of a todo item."""
    response = client.delete("/todos/1")
    assert response.status_code == 200
    response = client.get("/todos/1")
    assert response.status_code == 404
    response = client.get("/todos")
    data = response.json()
    assert len(data) == 0

def test_secure_todos_without_key() -> None:
    response = client.get("/secure-todos")
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation failed"
    assert len(data["details"]) > 0
    assert data["details"][0]["type"] == "missing"
    assert data["details"][0]["loc"] == ["header", "x-api-key"]
    assert data["details"][0]["msg"] == "Field required"

def test_secure_todos_with_key() -> None:
    response = client.get("/secure-todos", headers={"x-api-key": "secret-key"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_validation_error() -> None:
    response = client.post("/todos", json={})
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "Validation failed"
    assert "details" in body
