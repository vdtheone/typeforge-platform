"""
Accounts — Admin Configuration
================================
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserProfile

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    fields = (
        "display_name",
        "bio",
        "country",
        "avatar",
        "total_tests",
        "best_wpm",
        "avg_wpm",
        "avg_accuracy",
        "xp",
        "level",
        "streak_days",
    )
    readonly_fields = ("total_tests", "best_wpm", "avg_wpm", "avg_accuracy", "xp", "level")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = (
        "username",
        "email",
        "is_verified",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_verified", "is_active", "is_staff", "date_joined")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Verification", {"fields": ("is_verified",)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Additional Info",
            {
                "fields": ("email",),
            },
        ),
    )
