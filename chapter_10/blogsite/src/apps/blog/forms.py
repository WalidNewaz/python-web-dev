# ============================================================
# App Form: PostForm
# This form processes the content for a new blog post.
# ============================================================

from django import forms

class PostForm(forms.Form):
    """Form for creating blog posts."""

    title = forms.CharField(max_length=100, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)