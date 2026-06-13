"""
Analytics — Admin Configuration
=================================
"""

from django.contrib import admin

from .models import AnalyticsSnapshot, TypingSession


@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "period_type",
        "period_start",
        "total_tests",
        "avg_wpm",
        "best_wpm",
        "avg_accuracy",
    )
    list_filter = ("period_type", "period_start")
    search_fields = ("user__username",)
    date_hierarchy = "period_start"


@admin.register(TypingSession)
class TypingSessionAdmin(admin.ModelAdmin):
    list_display = ("result", "burst_speed_max", "burst_speed_avg", "created_at")
    readonly_fields = (
        "keystroke_log",
        "error_positions",
        "timing_data",
        "finger_speeds",
    )
