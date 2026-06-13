"""
Themes — Admin Configuration
==============================
"""

from django.contrib import admin

from .models import Theme, ThemeLike


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name", "creator", "is_default", "is_public", "likes_count", "usage_count")
    list_filter = ("is_default", "is_public")
    search_fields = ("name", "slug")
    readonly_fields = ("slug", "likes_count", "usage_count")


@admin.register(ThemeLike)
class ThemeLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "theme", "created_at")
    list_filter = ("created_at",)
