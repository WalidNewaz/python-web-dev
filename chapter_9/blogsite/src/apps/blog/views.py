# ============================================================
# App Views
# This file contains all the views.
# ============================================================

from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post


def home(request):
    """Handle GET (show form) and POST (save form to DB)."""
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "blog/home.html", {"posts": posts})

def create_post(request):
    """Handle GET (show form) and POST (process form)."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(**form.cleaned_data)
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})