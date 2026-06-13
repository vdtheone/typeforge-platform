"""
Leaderboards — Services
========================
Redis-backed leaderboard logic using sorted sets.
"""

import logging

from django.conf import settings
from django.core.cache import cache
from django.db.models import Avg, Count, Max

logger = logging.getLogger(__name__)


class LeaderboardService:
    """
    Leaderboard service using Redis sorted sets for O(log n) operations.
    Falls back to database queries when Redis is unavailable.
    """

    # Redis key patterns
    KEY_PATTERN = "leaderboard:{board_type}:{mode}:{duration}"
    CACHE_TTL = 300  # 5 minutes

    @classmethod
    def _get_redis_key(cls, board_type, mode="time", duration=60):
        return cls.KEY_PATTERN.format(
            board_type=board_type, mode=mode, duration=duration
        )

    @classmethod
    def update_score(cls, user_id, wpm, board_type="global", mode="time", duration=60):
        """
        Update a user's score on the leaderboard.
        Only updates if the new WPM is higher than existing.
        """
        key = cls._get_redis_key(board_type, mode, duration)
        try:
            from django_redis import get_redis_connection

            redis_conn = get_redis_connection("default")
            # ZADD with GT flag — only update if new score is greater
            redis_conn.zadd(key, {str(user_id): wpm}, gt=True)
        except Exception as e:
            logger.warning("Redis leaderboard update failed: %s", e)
            # Fallback: update database
            cls._update_db_entry(user_id, wpm, board_type, mode, duration)

    @classmethod
    def get_leaderboard(cls, board_type="global", mode="time", duration=60,
                        offset=0, limit=50):
        """
        Get leaderboard rankings.
        Returns list of {user_id, wpm, rank} dicts.
        """
        key = cls._get_redis_key(board_type, mode, duration)
        cache_key = f"lb_result:{key}:{offset}:{limit}"

        # Check cache first
        cached = cache.get(cache_key)
        if cached:
            return cached

        try:
            from django_redis import get_redis_connection

            redis_conn = get_redis_connection("default")
            # ZREVRANGE with scores (highest first)
            results = redis_conn.zrevrange(key, offset, offset + limit - 1, withscores=True)

            leaderboard = []
            for rank, (user_id_bytes, score) in enumerate(results, start=offset + 1):
                leaderboard.append({
                    "user_id": int(user_id_bytes),
                    "wpm": round(float(score), 2),
                    "rank": rank,
                })

            cache.set(cache_key, leaderboard, cls.CACHE_TTL)
            return leaderboard

        except Exception as e:
            logger.warning("Redis leaderboard read failed: %s", e)
            return cls._get_db_leaderboard(board_type, mode, duration, offset, limit)

    @classmethod
    def get_user_rank(cls, user_id, board_type="global", mode="time", duration=60):
        """Get a specific user's rank on the leaderboard."""
        key = cls._get_redis_key(board_type, mode, duration)
        try:
            from django_redis import get_redis_connection

            redis_conn = get_redis_connection("default")
            rank = redis_conn.zrevrank(key, str(user_id))
            score = redis_conn.zscore(key, str(user_id))
            if rank is not None:
                return {
                    "rank": rank + 1,  # 0-indexed to 1-indexed
                    "wpm": round(float(score), 2),
                }
        except Exception:
            pass

        return None

    @classmethod
    def _update_db_entry(cls, user_id, wpm, board_type, mode, duration):
        """Fallback: update leaderboard entry in database."""
        from .models import LeaderboardEntry

        entry, created = LeaderboardEntry.objects.get_or_create(
            user_id=user_id,
            board_type=board_type,
            mode=mode,
            duration=duration,
            period_start=None,
            defaults={"best_wpm": wpm},
        )
        if not created and wpm > entry.best_wpm:
            entry.best_wpm = wpm
            entry.save(update_fields=["best_wpm", "updated_at"])

    @classmethod
    def _get_db_leaderboard(cls, board_type, mode, duration, offset, limit):
        """Fallback: get leaderboard from database."""
        from .models import LeaderboardEntry

        entries = (
            LeaderboardEntry.objects.filter(
                board_type=board_type,
                mode=mode,
                duration=duration,
            )
            .select_related("user")
            .order_by("-best_wpm")[offset : offset + limit]
        )

        return [
            {
                "user_id": entry.user_id,
                "wpm": entry.best_wpm,
                "rank": offset + idx + 1,
            }
            for idx, entry in enumerate(entries)
        ]
