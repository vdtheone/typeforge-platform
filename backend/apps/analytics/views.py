"""
Analytics — Views
==================
"""

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DashboardSerializer
from .services import AnalyticsService


class AnalyticsDashboardView(APIView):
    """
    GET /api/v1/analytics/dashboard/ — Get analytics dashboard summary
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = AnalyticsService.get_dashboard_data(request.user)
        serializer = DashboardSerializer(data)
        return Response({"success": True, "data": serializer.data})


class WPMTrendView(APIView):
    """
    GET /api/v1/analytics/wpm-trend/ — Get WPM trend over time
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        days = min(max(days, 7), 365)  # Clamp between 7 and 365

        trend = AnalyticsService.get_wpm_trend(request.user, days=days)
        data = [
            {
                "date": item["date"].isoformat(),
                "avg_wpm": round(item["avg_wpm"], 2),
                "best_wpm": round(item["best_wpm"], 2),
                "tests_count": item["tests_count"],
            }
            for item in trend
        ]
        return Response({"success": True, "data": data})


class AccuracyTrendView(APIView):
    """
    GET /api/v1/analytics/accuracy-trend/ — Get accuracy trend over time
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        days = min(max(days, 7), 365)

        trend = AnalyticsService.get_accuracy_trend(request.user, days=days)
        data = [
            {
                "date": item["date"].isoformat(),
                "avg_accuracy": round(item["avg_accuracy"], 2),
                "tests_count": item["tests_count"],
            }
            for item in trend
        ]
        return Response({"success": True, "data": data})


class WeakKeysView(APIView):
    """
    GET /api/v1/analytics/weak-keys/ — Get weak key analysis
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from apps.results.models import Result

        results = (
            Result.objects.filter(user=request.user, is_flagged=False)
            .order_by("-created_at")[:100]
        )
        weak_keys = AnalyticsService._compute_weak_keys(results)
        return Response({"success": True, "data": weak_keys})
