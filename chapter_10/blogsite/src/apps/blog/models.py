# ============================================================
# App Models
# This file contains all the models.
# ============================================================

from django.db import models

class Post(models.Model):
    """Database model for blog posts."""

    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a human-readable representation."""
        return f"Post: {self.id} - {self.title} ({self.created_at:%Y-%m-%d})"
