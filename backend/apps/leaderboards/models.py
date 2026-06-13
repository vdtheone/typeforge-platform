"""
Leaderboards — Models
======================
"""

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class LeaderboardEntry(TimeStampedModel):
    """
    Cached leaderboard entries.
    These are periodically refreshed from results data.
    Primary leaderboard data lives in Redis sorted sets for O(log n) ranking.
    This model serves as a persistent fallback and for complex queries.
    """

    class BoardType(models.TextChoices):
        GLOBAL = "global", "All Time"
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leaderboard_entries",
    )
    board_type = models.CharField(max_length=10, choices=BoardType.choices)
    mode = models.CharField(max_length=20, default="time")
    duration = models.PositiveIntegerField(default=60)

    # Scores
    best_wpm = models.FloatField(default=0.0)
    avg_wpm = models.FloatField(default=0.0)
    best_accuracy = models.FloatField(default=0.0)
    total_tests = models.PositiveIntegerField(default=0)

    # Ranking (computed)
    rank = models.PositiveIntegerField(default=0)

    # Period tracking
    period_start = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "leaderboard_entries"
        verbose_name = "Leaderboard Entry"
        verbose_name_plural = "Leaderboard Entries"
        ordering = ["-best_wpm"]
        indexes = [
            models.Index(fields=["board_type", "mode", "duration", "-best_wpm"]),
            models.Index(fields=["board_type", "-best_wpm"]),
        ]
        unique_together = ("user", "board_type", "mode", "duration", "period_start")

    def __str__(self):
        return f"#{self.rank} {self.user.username}: {self.best_wpm} WPM ({self.board_type})"
