import pytest
from django.test import Client

@pytest.mark.django_db
def test_home_view():
    """Home page test"""
    client = Client()
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello, Django Blog!" in response.content.decode()