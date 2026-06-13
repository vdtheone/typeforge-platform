"""
Leaderboards — Admin Configuration
=====================================
"""

from django.contrib import admin

from .models import LeaderboardEntry


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "board_type", "mode", "duration", "best_wpm", "rank")
    list_filter = ("board_type", "mode", "duration")
    search_fields = ("user__username",)
    ordering = ("-best_wpm",)
