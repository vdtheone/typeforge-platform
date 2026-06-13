"""
Analytics — Services
=====================
Analytics computation logic.
"""

from collections import Counter, defaultdict
from datetime import timedelta

from django.db.models import Avg, Count, Max, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from apps.results.models import Result


class AnalyticsService:
    """Computes analytics data for users."""

    @classmethod
    def get_dashboard_data(cls, user):
        """Generate complete dashboard summary for a user."""
        results = Result.objects.filter(user=user, is_flagged=False)

        # Overall stats
        stats = results.aggregate(
            total_tests=Count("id"),
            total_time_seconds=Sum("duration"),
            avg_wpm=Avg("wpm"),
            best_wpm=Max("wpm"),
            avg_accuracy=Avg("accuracy"),
            avg_consistency=Avg("consistency"),
        )

        # Fill None defaults
        for key in stats:
            if stats[key] is None:
                stats[key] = 0
        for key in ["avg_wpm", "avg_accuracy", "avg_consistency"]:
            stats[key] = round(stats[key], 2)

        # Recent WPM trend (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        wpm_trend = (
            results.filter(created_at__gte=thirty_days_ago)
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(
                avg_wpm=Avg("wpm"),
                best_wpm=Max("wpm"),
                tests_count=Count("id"),
            )
            .order_by("date")
        )

        # Recent accuracy trend
        accuracy_trend = (
            results.filter(created_at__gte=thirty_days_ago)
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(
                avg_accuracy=Avg("accuracy"),
                tests_count=Count("id"),
            )
            .order_by("date")
        )

        # Weak key analysis
        weak_keys = cls._compute_weak_keys(results.order_by("-created_at")[:50])

        # Level & XP
        profile = user.profile

        return {
            **stats,
            "recent_wpm_trend": [
                {
                    "date": item["date"].isoformat(),
                    "avg_wpm": round(item["avg_wpm"], 2),
                    "best_wpm": round(item["best_wpm"], 2),
                    "tests_count": item["tests_count"],
                }
                for item in wpm_trend
            ],
            "recent_accuracy_trend": [
                {
                    "date": item["date"].isoformat(),
                    "avg_accuracy": round(item["avg_accuracy"], 2),
                    "tests_count": item["tests_count"],
                }
                for item in accuracy_trend
            ],
            "weak_keys": weak_keys,
            "level": profile.level,
            "xp": profile.xp,
            "xp_to_next_level": ((profile.level) * 100) - profile.xp,
        }

    @classmethod
    def get_wpm_trend(cls, user, days=30):
        """Get WPM trend data over the specified number of days."""
        start_date = timezone.now() - timedelta(days=days)
        return (
            Result.objects.filter(
                user=user,
                is_flagged=False,
                created_at__gte=start_date,
            )
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(
                avg_wpm=Avg("wpm"),
                best_wpm=Max("wpm"),
                tests_count=Count("id"),
            )
            .order_by("date")
        )

    @classmethod
    def get_accuracy_trend(cls, user, days=30):
        """Get accuracy trend data."""
        start_date = timezone.now() - timedelta(days=days)
        return (
            Result.objects.filter(
                user=user,
                is_flagged=False,
                created_at__gte=start_date,
            )
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(
                avg_accuracy=Avg("accuracy"),
                tests_count=Count("id"),
            )
            .order_by("date")
        )

    @classmethod
    def _compute_weak_keys(cls, results):
        """Analyze char_log data to find weak keys."""
        error_counts = Counter()
        total_counts = Counter()

        for result in results:
            char_log = result.char_log
            if not isinstance(char_log, list):
                continue

            for entry in char_log:
                if isinstance(entry, dict):
                    char = entry.get("char", "")
                    state = entry.get("state", "")
                    if char:
                        total_counts[char] += 1
                        if state == "incorrect":
                            error_counts[char] += 1

        # Calculate error rates
        weak_keys = {}
        for char, errors in error_counts.most_common(10):
            total = total_counts[char]
            if total >= 5:  # Only include keys with enough data
                weak_keys[char] = {
                    "error_count": errors,
                    "total_count": total,
                    "error_rate": round((errors / total) * 100, 2),
                }

        return weak_keys
