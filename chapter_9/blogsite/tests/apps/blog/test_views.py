import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_home_page_renders():
    client = Client()
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert "Welcome to the Blog" in response.content.decode()


@pytest.mark.django_db
def test_create_post_form():
    client = Client()
    response = client.post(reverse("create_post"), {"title": "My First Post", "content": "Hello"})
    assert response.status_code == 302  # Redirect after success

    response = client.get(reverse("home"))
    body = response.content.decode()
    assert "My First Post" in body
    assert "Hello" in body