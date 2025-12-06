import pytest
from tests.test_utils import create_test_app

@pytest.fixture(scope="session")
def client():
    client = create_test_app()
    # seed_test_user()
    return client


@pytest.fixture(scope="session")
def auth_token(client):
    response = client.post(
        "/auth/token",
        data={
            "username": "alice",
            "password": "wonderland",
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]
