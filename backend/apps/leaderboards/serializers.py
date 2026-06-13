"""
Leaderboards — Serializers
============================
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LeaderboardEntrySerializer(serializers.Serializer):
    """Serializer for leaderboard entries."""

    rank = serializers.IntegerField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    wpm = serializers.FloatField()
    country = serializers.CharField(required=False, default="")
    level = serializers.IntegerField(required=False, default=1)


class LeaderboardQuerySerializer(serializers.Serializer):
    """Serializer for leaderboard query parameters."""

    mode = serializers.ChoiceField(
        choices=["time", "words", "quote"], default="time"
    )
    duration = serializers.ChoiceField(
        choices=[15, 30, 60, 120], default=60
    )
    page = serializers.IntegerField(min_value=1, default=1)
    page_size = serializers.IntegerField(min_value=10, max_value=100, default=50)
