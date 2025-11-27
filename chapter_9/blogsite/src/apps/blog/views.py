# ============================================================
# App Views
# This file contains all the views.
# ============================================================

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import PostForm

# Temporary storage for posts
POSTS = []

def home(request):
    """Render homepage with all blog posts."""
    return render(request, "blog/home.html", {"posts": POSTS})

def create_post(request):
    """Handle GET (show form) and POST (process form)."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            POSTS.append(form.cleaned_data)
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})