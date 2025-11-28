# ============================================================
# Register App Models with the Admin
# ============================================================

from django.contrib import admin

from .models import Post

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "created_at")
    search_fields = ("title","content")
    list_filter = ("created_at",)

