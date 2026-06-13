"""
Results — Serializers
======================
"""

from rest_framework import serializers

from .models import Result


class ResultSerializer(serializers.ModelSerializer):
    """Full result serializer including all data."""

    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Result
        fields = [
            "id",
            "username",
            "wpm",
            "raw_wpm",
            "accuracy",
            "consistency",
            "mode",
            "duration",
            "language",
            "characters_typed",
            "correct_chars",
            "incorrect_chars",
            "extra_chars",
            "missed_chars",
            "wpm_history",
            "is_personal_best",
            "is_flagged",
            "created_at",
        ]
        read_only_fields = fields


class ResultDetailSerializer(ResultSerializer):
    """Result detail with full keystroke and char log data."""

    class Meta(ResultSerializer.Meta):
        fields = ResultSerializer.Meta.fields + ["keystrokes", "char_log"]


class ResultSummarySerializer(serializers.ModelSerializer):
    """Lightweight result serializer for listings."""

    class Meta:
        model = Result
        fields = [
            "id",
            "wpm",
            "raw_wpm",
            "accuracy",
            "consistency",
            "mode",
            "duration",
            "language",
            "is_personal_best",
            "created_at",
        ]


class ResultStatsSerializer(serializers.Serializer):
    """Serializer for aggregated result statistics."""

    total_tests = serializers.IntegerField()
    total_time_seconds = serializers.IntegerField()
    avg_wpm = serializers.FloatField()
    best_wpm = serializers.FloatField()
    avg_accuracy = serializers.FloatField()
    avg_consistency = serializers.FloatField()
    best_accuracy = serializers.FloatField()
    tests_last_24h = serializers.IntegerField()
    tests_last_7d = serializers.IntegerField()
