"""
Leaderboards — URLs
====================
"""

from django.urls import path

from . import views

urlpatterns = [
    path("global/", views.GlobalLeaderboardView.as_view(), name="leaderboard-global"),
    path("daily/", views.DailyLeaderboardView.as_view(), name="leaderboard-daily"),
    path("weekly/", views.WeeklyLeaderboardView.as_view(), name="leaderboard-weekly"),
]
