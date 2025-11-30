# ============================================================
# App Form: PostForm
# This form processes the content for a new blog post.
# ============================================================

from django import forms
from .models import Post

class PostForm(forms.Form):
    """Form for creating blog posts."""

    title = forms.CharField(max_length=100, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title