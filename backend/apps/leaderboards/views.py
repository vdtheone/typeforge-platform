"""
Leaderboards — Views
=====================
"""

from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LeaderboardEntrySerializer, LeaderboardQuerySerializer
from .services import LeaderboardService

User = get_user_model()


class BaseLeaderboardView(APIView):
    """Base view for leaderboard endpoints."""

    permission_classes = [permissions.AllowAny]
    board_type = "global"

    def get(self, request):
        query_serializer = LeaderboardQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        params = query_serializer.validated_data

        page = params["page"]
        page_size = params["page_size"]
        offset = (page - 1) * page_size

        # Get leaderboard data
        entries = LeaderboardService.get_leaderboard(
            board_type=self.board_type,
            mode=params["mode"],
            duration=params["duration"],
            offset=offset,
            limit=page_size,
        )

        # Enrich with user data
        user_ids = [e["user_id"] for e in entries]
        users = User.objects.filter(id__in=user_ids).select_related("profile")
        user_map = {u.id: u for u in users}

        enriched = []
        for entry in entries:
            user = user_map.get(entry["user_id"])
            if user:
                enriched.append({
                    "rank": entry["rank"],
                    "user_id": entry["user_id"],
                    "username": user.username,
                    "wpm": entry["wpm"],
                    "country": getattr(user.profile, "country", ""),
                    "level": getattr(user.profile, "level", 1),
                })

        serializer = LeaderboardEntrySerializer(enriched, many=True)

        # Include current user's rank if authenticated
        user_rank = None
        if request.user.is_authenticated:
            user_rank = LeaderboardService.get_user_rank(
                request.user.id,
                board_type=self.board_type,
                mode=params["mode"],
                duration=params["duration"],
            )

        return Response({
            "success": True,
            "data": {
                "entries": serializer.data,
                "page": page,
                "page_size": page_size,
                "user_rank": user_rank,
            },
        })


class GlobalLeaderboardView(BaseLeaderboardView):
    """GET /api/v1/leaderboards/global/"""

    board_type = "global"


class DailyLeaderboardView(BaseLeaderboardView):
    """GET /api/v1/leaderboards/daily/"""

    board_type = "daily"


class WeeklyLeaderboardView(BaseLeaderboardView):
    """GET /api/v1/leaderboards/weekly/"""

    board_type = "weekly"
