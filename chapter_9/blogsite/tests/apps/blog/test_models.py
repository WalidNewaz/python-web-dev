import pytest
from django.urls import reverse
from apps.blog.models import Post

@pytest.mark.django_db
def test_post_creation_and_query():
    post = Post.objects.create(title="Test Post", content="Hello ORM")
    assert Post.objects.count() == 1
    assert "Test Post" in str(post)

    posts = Post.objects.filter(title__icontains="test")
    assert posts.exists()
    assert posts.first().content == "Hello ORM"


@pytest.mark.django_db
def test_home_view_displays_posts(client):
    Post.objects.create(title="Visible Post", content="This should appear")
    response = client.get(reverse("home"))
    assert response.status_code == 200
    body = response.content.decode()
    assert "Visible Post" in body