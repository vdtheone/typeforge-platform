"""
Results — Views
================
"""

from datetime import timedelta

from django.db.models import Avg, Count, Max, Sum
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.pagination import StandardResultsSetPagination

from .models import Result
from .serializers import (
    ResultDetailSerializer,
    ResultStatsSerializer,
    ResultSummarySerializer,
)


class ResultListView(generics.ListAPIView):
    """
    GET /api/v1/results/ — List current user's results
    """

    serializer_class = ResultSummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["mode", "language"]
    ordering_fields = ["wpm", "accuracy", "consistency", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user)


class ResultDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/results/<id>/ — Get detailed result with replay data
    """

    serializer_class = ResultDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user)


class ResultStatsView(APIView):
    """
    GET /api/v1/results/stats/ — Get aggregated typing statistics
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        results = Result.objects.filter(user=request.user, is_flagged=False)

        stats = results.aggregate(
            total_tests=Count("id"),
            total_time_seconds=Sum("duration"),
            avg_wpm=Avg("wpm"),
            best_wpm=Max("wpm"),
            avg_accuracy=Avg("accuracy"),
            avg_consistency=Avg("consistency"),
            best_accuracy=Max("accuracy"),
        )

        # Fill None values with defaults
        for key in stats:
            if stats[key] is None:
                stats[key] = 0

        # Round float values
        for key in ["avg_wpm", "avg_accuracy", "avg_consistency"]:
            stats[key] = round(stats[key], 2)

        stats["tests_last_24h"] = results.filter(
            created_at__gte=now - timedelta(hours=24)
        ).count()
        stats["tests_last_7d"] = results.filter(
            created_at__gte=now - timedelta(days=7)
        ).count()

        serializer = ResultStatsSerializer(stats)
        return Response({"success": True, "data": serializer.data})


class PersonalBestsView(APIView):
    """
    GET /api/v1/results/personal-bests/ — Get personal best results
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pbs = (
            Result.objects.filter(
                user=request.user,
                is_personal_best=True,
                is_flagged=False,
            )
            .select_related("user")
            .order_by("mode", "duration")
        )

        serializer = ResultSummarySerializer(pbs, many=True)
        return Response({"success": True, "data": serializer.data})
