"""
Typing Tests — Serializers
============================
"""

from rest_framework import serializers

from apps.typing_tests.services import TestGenerationService


class TestGenerateSerializer(serializers.Serializer):
    """Serializer for test generation request parameters."""

    mode = serializers.ChoiceField(
        choices=TestGenerationService.VALID_MODES,
        default="time",
    )
    language = serializers.CharField(max_length=10, default="en")
    duration = serializers.ChoiceField(
        choices=TestGenerationService.VALID_DURATIONS,
        default=30,
        required=False,
    )
    word_count = serializers.ChoiceField(
        choices=TestGenerationService.VALID_WORD_COUNTS,
        default=50,
        required=False,
    )
    wordlist_id = serializers.IntegerField(required=False)
    difficulty = serializers.ChoiceField(
        choices=["beginner", "easy", "medium", "hard", "expert"],
        required=False,
    )
    punctuation = serializers.BooleanField(default=False)
    numbers = serializers.BooleanField(default=False)


class TestSubmitSerializer(serializers.Serializer):
    """Serializer for typing test submission."""

    # Test configuration
    mode = serializers.ChoiceField(choices=TestGenerationService.VALID_MODES)
    duration = serializers.IntegerField(min_value=1, max_value=600)
    language = serializers.CharField(max_length=10, default="en")
    wordlist_id = serializers.IntegerField(required=False, allow_null=True)

    # Performance metrics
    wpm = serializers.FloatField(min_value=0, max_value=500)
    raw_wpm = serializers.FloatField(min_value=0, max_value=500)
    accuracy = serializers.FloatField(min_value=0, max_value=100)
    consistency = serializers.FloatField(min_value=0, max_value=100)

    # Typing data
    characters_typed = serializers.IntegerField(min_value=0)
    correct_chars = serializers.IntegerField(min_value=0)
    incorrect_chars = serializers.IntegerField(min_value=0)
    extra_chars = serializers.IntegerField(min_value=0, default=0)
    missed_chars = serializers.IntegerField(min_value=0, default=0)

    # Detailed data
    keystrokes = serializers.JSONField(required=False, default=list)
    char_log = serializers.JSONField(required=False, default=list)
    wpm_history = serializers.JSONField(
        required=False,
        default=list,
        help_text="WPM values at each second for consistency calculation",
    )

    def validate(self, data):
        # Basic sanity checks
        if data["correct_chars"] + data["incorrect_chars"] > data["characters_typed"] * 2:
            raise serializers.ValidationError(
                "Character counts don't add up correctly."
            )
        return data
