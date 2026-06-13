"""
Leaderboards — Celery Tasks
=============================
"""

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="apps.leaderboards.tasks.refresh_daily_leaderboard")
def refresh_daily_leaderboard():
    """
    Hourly task: refresh daily leaderboard from today's results.
    """
    from datetime import date

    from django.db.models import Max

    from apps.results.models import Result

    logger.info("Refreshing daily leaderboard")

    today = date.today()
    from .services import LeaderboardService

    # Get today's best WPM per user
    user_bests = (
        Result.objects.filter(
            created_at__date=today,
            is_flagged=False,
        )
        .values("user_id")
        .annotate(best_wpm=Max("wpm"))
    )

    for entry in user_bests:
        LeaderboardService.update_score(
            user_id=entry["user_id"],
            wpm=entry["best_wpm"],
            board_type="daily",
        )

    logger.info("Daily leaderboard refreshed with %d entries", len(user_bests))
