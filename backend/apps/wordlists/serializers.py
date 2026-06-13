"""
Word Lists — Serializers
=========================
"""

from rest_framework import serializers

from .models import Language, Quote, WordList


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name", "code", "flag_emoji", "is_active"]


class WordListSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)
    language_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.filter(is_active=True),
        source="language",
        write_only=True,
    )
    creator_username = serializers.CharField(source="creator.username", read_only=True)

    class Meta:
        model = WordList
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "words",
            "word_count",
            "language",
            "language_id",
            "difficulty",
            "creator_username",
            "is_public",
            "is_default",
            "times_used",
            "created_at",
        ]
        read_only_fields = ["slug", "word_count", "times_used", "is_default", "created_at"]

    def validate_words(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Words must be a JSON array.")
        if len(value) < 10:
            raise serializers.ValidationError("Word list must contain at least 10 words.")
        if len(value) > 50000:
            raise serializers.ValidationError("Word list cannot exceed 50,000 words.")
        # Ensure all items are strings
        if not all(isinstance(w, str) for w in value):
            raise serializers.ValidationError("All items in the word list must be strings.")
        return value


class WordListSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing (no words array)."""

    language_code = serializers.CharField(source="language.code", read_only=True)

    class Meta:
        model = WordList
        fields = [
            "id",
            "name",
            "slug",
            "word_count",
            "language_code",
            "difficulty",
            "is_default",
            "times_used",
        ]


class QuoteSerializer(serializers.ModelSerializer):
    language_code = serializers.CharField(source="language.code", read_only=True)

    class Meta:
        model = Quote
        fields = [
            "id",
            "text",
            "source",
            "author",
            "language_code",
            "word_count",
            "char_count",
            "difficulty",
        ]
