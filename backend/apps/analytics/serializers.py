"""
Analytics — Serializers
========================
"""

from rest_framework import serializers

from .models import AnalyticsSnapshot


class AnalyticsSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsSnapshot
        fields = [
            "id",
            "period_type",
            "period_start",
            "period_end",
            "total_tests",
            "total_time_seconds",
            "avg_wpm",
            "best_wpm",
            "avg_accuracy",
            "avg_consistency",
            "avg_raw_wpm",
            "weak_keys",
            "wpm_distribution",
            "accuracy_distribution",
            "metrics",
        ]


class DashboardSerializer(serializers.Serializer):
    """Serializer for the analytics dashboard summary."""

    # Overall Stats
    total_tests = serializers.IntegerField()
    total_time_seconds = serializers.IntegerField()
    avg_wpm = serializers.FloatField()
    best_wpm = serializers.FloatField()
    avg_accuracy = serializers.FloatField()
    avg_consistency = serializers.FloatField()

    # Recent Performance
    recent_wpm_trend = serializers.ListField(child=serializers.DictField())
    recent_accuracy_trend = serializers.ListField(child=serializers.DictField())

    # Weak Keys
    weak_keys = serializers.DictField()

    # Level & XP
    level = serializers.IntegerField()
    xp = serializers.IntegerField()
    xp_to_next_level = serializers.IntegerField()


class WPMTrendSerializer(serializers.Serializer):
    """Serializer for WPM trend data."""

    date = serializers.DateField()
    avg_wpm = serializers.FloatField()
    best_wpm = serializers.FloatField()
    tests_count = serializers.IntegerField()


class WeakKeySerializer(serializers.Serializer):
    """Serializer for weak key analysis."""

    key = serializers.CharField()
    error_count = serializers.IntegerField()
    total_count = serializers.IntegerField()
    error_rate = serializers.FloatField()
