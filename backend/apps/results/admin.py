"""
Results — Admin Configuration
===============================
"""

from django.contrib import admin

from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "wpm",
        "raw_wpm",
        "accuracy",
        "consistency",
        "mode",
        "duration",
        "language",
        "is_personal_best",
        "is_flagged",
        "created_at",
    )
    list_filter = ("mode", "language", "is_personal_best", "is_flagged", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("is_personal_best", "is_flagged", "flag_reasons")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("User", {"fields": ("user",)}),
        (
            "Performance",
            {"fields": ("wpm", "raw_wpm", "accuracy", "consistency")},
        ),
        (
            "Test Config",
            {"fields": ("mode", "duration", "language", "wordlist")},
        ),
        (
            "Characters",
            {
                "fields": (
                    "characters_typed",
                    "correct_chars",
                    "incorrect_chars",
                    "extra_chars",
                    "missed_chars",
                )
            },
        ),
        (
            "Anti-Cheat",
            {"fields": ("is_flagged", "flag_reasons", "is_personal_best")},
        ),
    )
