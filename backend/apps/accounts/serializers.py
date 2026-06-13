"""
Accounts — Serializers
=======================
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile

User = get_user_model()


# =============================================================================
# JWT Serializers
# =============================================================================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer that includes user data in the token claims."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        return token


class CustomJWTSerializer(serializers.Serializer):
    """Serializer for JWT response with user data."""

    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.get("user") or self.context.get("request").user
        return UserSummarySerializer(user).data


# =============================================================================
# Registration
# =============================================================================
class CustomRegisterSerializer(serializers.Serializer):
    """Registration serializer with username + email + password."""

    username = serializers.CharField(min_length=3, max_length=30)
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        # Only allow alphanumeric + underscore
        if not value.replace("_", "").isalnum():
            raise serializers.ValidationError(
                "Username may only contain letters, numbers, and underscores."
            )
        return value.lower()

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value.lower()

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data

    def get_cleaned_data(self):
        return {
            "username": self.validated_data["username"],
            "email": self.validated_data["email"],
            "password1": self.validated_data["password1"],
        }

    def save(self, request):
        from allauth.account.adapter import get_adapter

        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        user.username = self.cleaned_data["username"]
        user.save()
        adapter.stash_verified_email(request, self.cleaned_data["email"])
        return user


# =============================================================================
# User Serializers
# =============================================================================
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""

    class Meta:
        model = UserProfile
        fields = [
            "display_name",
            "bio",
            "avatar",
            "country",
            "total_tests",
            "total_time_typing",
            "best_wpm",
            "avg_wpm",
            "avg_accuracy",
            "xp",
            "level",
            "streak_days",
            "preferences",
        ]
        read_only_fields = [
            "total_tests",
            "total_time_typing",
            "best_wpm",
            "avg_wpm",
            "avg_accuracy",
            "xp",
            "level",
            "streak_days",
        ]


class UserSummarySerializer(serializers.ModelSerializer):
    """Lightweight user serializer for embedding in other responses."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]


class UserDetailSerializer(serializers.ModelSerializer):
    """Full user detail serializer with profile data."""

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_verified",
            "date_joined",
            "last_login",
            "profile",
        ]
        read_only_fields = ["id", "email", "is_verified", "date_joined", "last_login"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update profile fields
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


class UserPreferencesSerializer(serializers.Serializer):
    """Serializer for user typing preferences."""

    caret_style = serializers.ChoiceField(
        choices=UserProfile.CaretStyle.choices, required=False
    )
    smooth_caret = serializers.BooleanField(required=False)
    sound_on_click = serializers.BooleanField(required=False)
    sound_on_error = serializers.BooleanField(required=False)
    show_live_wpm = serializers.BooleanField(required=False)
    show_live_accuracy = serializers.BooleanField(required=False)
    font_family = serializers.CharField(max_length=100, required=False)
    font_size = serializers.IntegerField(min_value=12, max_value=36, required=False)
    strict_space = serializers.BooleanField(required=False)
    freedom_mode = serializers.BooleanField(required=False)
    blind_mode = serializers.BooleanField(required=False)


class PublicProfileSerializer(serializers.ModelSerializer):
    """Public profile view — no email, limited data."""

    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "date_joined", "profile"]

    def get_profile(self, obj):
        if hasattr(obj, "profile"):
            return {
                "display_name": obj.profile.display_name,
                "avatar": obj.profile.avatar.url if obj.profile.avatar else None,
                "country": obj.profile.country,
                "total_tests": obj.profile.total_tests,
                "best_wpm": obj.profile.best_wpm,
                "avg_wpm": obj.profile.avg_wpm,
                "level": obj.profile.level,
                "xp": obj.profile.xp,
            }
        return None
