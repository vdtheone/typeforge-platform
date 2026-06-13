"""
Themes — Serializers
=====================
"""

from rest_framework import serializers

from .models import Theme


class ThemeSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source="creator.username", read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "css_variables",
            "preview_image",
            "creator_username",
            "is_public",
            "is_default",
            "likes_count",
            "usage_count",
            "is_liked",
            "created_at",
        ]
        read_only_fields = [
            "slug",
            "is_default",
            "likes_count",
            "usage_count",
            "created_at",
        ]

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def validate_css_variables(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("CSS variables must be a JSON object.")
        required_vars = ["--bg-color", "--text-color", "--sub-color"]
        missing = [v for v in required_vars if v not in value]
        if missing:
            raise serializers.ValidationError(
                f"Missing required CSS variables: {', '.join(missing)}"
            )
        return value


class ThemeSummarySerializer(serializers.ModelSerializer):
    """Lightweight theme serializer for listings."""

    class Meta:
        model = Theme
        fields = [
            "id",
            "name",
            "slug",
            "is_default",
            "likes_count",
            "preview_image",
        ]
