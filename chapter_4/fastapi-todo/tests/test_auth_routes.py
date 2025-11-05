from fastapi.testclient import TestClient
from fastapi_todo.main import app

client = TestClient(app)

def test_login_and_secure_access() -> None:
    """Login to get a token."""
    response = client.post("/login", data={"username": "alice", "password": "wonderland"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Use token to access secure route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/secure-todos", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_invalid_login() -> None:
    response = client.post("/login", data={"username": "alice", "password": "wrong"})
    assert response.status_code == 401

def test_secure_route_without_token() -> None:
    response = client.get("/secure-todos")
    assert response.status_code == 401
