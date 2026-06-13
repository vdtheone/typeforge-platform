"""
Analytics — Celery Tasks
=========================
"""

import logging
from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Max, Sum
from django.utils import timezone

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task(name="apps.analytics.tasks.aggregate_daily_analytics")
def aggregate_daily_analytics():
    """
    Daily task: compute and store analytics snapshots for all active users.
    """
    from apps.analytics.models import AnalyticsSnapshot
    from apps.results.models import Result

    yesterday = timezone.now().date() - timedelta(days=1)
    logger.info("Aggregating daily analytics for %s", yesterday)

    # Get users who had activity yesterday
    active_users = (
        Result.objects.filter(created_at__date=yesterday)
        .values_list("user_id", flat=True)
        .distinct()
    )

    for user_id in active_users:
        results = Result.objects.filter(
            user_id=user_id,
            created_at__date=yesterday,
            is_flagged=False,
        )

        stats = results.aggregate(
            total_tests=Count("id"),
            total_time_seconds=Sum("duration"),
            avg_wpm=Avg("wpm"),
            best_wpm=Max("wpm"),
            avg_accuracy=Avg("accuracy"),
            avg_consistency=Avg("consistency"),
            avg_raw_wpm=Avg("raw_wpm"),
        )

        # Fill None values
        for key in stats:
            if stats[key] is None:
                stats[key] = 0

        # WPM distribution
        wpm_values = list(results.values_list("wpm", flat=True))

        AnalyticsSnapshot.objects.update_or_create(
            user_id=user_id,
            period_type="daily",
            period_start=yesterday,
            defaults={
                "period_end": yesterday,
                "total_tests": stats["total_tests"],
                "total_time_seconds": stats["total_time_seconds"] or 0,
                "avg_wpm": round(stats["avg_wpm"], 2),
                "best_wpm": round(stats["best_wpm"], 2),
                "avg_accuracy": round(stats["avg_accuracy"], 2),
                "avg_consistency": round(stats["avg_consistency"], 2),
                "avg_raw_wpm": round(stats["avg_raw_wpm"], 2),
                "wpm_distribution": wpm_values,
            },
        )

    logger.info("Daily analytics aggregated for %d users", len(active_users))
