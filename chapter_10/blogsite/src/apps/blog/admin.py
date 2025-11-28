# ============================================================
# Register App Models with the Admin
# ============================================================

from django.contrib import admin

from django.contrib import admin
from .models import Post

admin.site.register(Post)