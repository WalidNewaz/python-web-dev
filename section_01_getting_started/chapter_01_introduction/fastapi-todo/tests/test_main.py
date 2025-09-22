from fastapi.testclient import TestClient
from fastapi_todo.main import app

client = TestClient(app)

def test_read_root():
    """Test that the root endpoint returns the correct JSON response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}