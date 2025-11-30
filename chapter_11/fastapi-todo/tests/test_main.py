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

def test_read_root() -> None:
    """Test that the root endpoint returns the correct JSON response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}


