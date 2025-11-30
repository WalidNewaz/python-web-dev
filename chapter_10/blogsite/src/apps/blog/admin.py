# ============================================================
# Register App Models with the Admin
# ============================================================

from django.contrib import admin

from .models import Post
from .forms import PostAdminForm

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ("id", "title", "content", "created_at")
    search_fields = ("title","content")
    list_filter = ("created_at",)
    fieldsets = (
        ("Post Information", {
            "fields": ("title", "content")
        }),
    )

