"""
Accounts — User & Profile Models
==================================
"""

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from apps.core.models import TimeStampedModel

from .managers import CustomUserManager


class User(AbstractUser):
    """
    Custom User model with email as the primary authentication field.
    """

    email = models.EmailField(
        unique=True,
        db_index=True,
        help_text="Required. A valid email address.",
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        validators=[MinLengthValidator(3)],
        help_text="Required. 3-30 characters.",
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether the user's email has been verified.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username


class UserProfile(TimeStampedModel):
    """
    Extended user profile with typing-specific data and preferences.
    """

    class Country(models.TextChoices):
        US = "US", "United States"
        GB = "GB", "United Kingdom"
        IN = "IN", "India"
        CA = "CA", "Canada"
        AU = "AU", "Australia"
        DE = "DE", "Germany"
        FR = "FR", "France"
        JP = "JP", "Japan"
        BR = "BR", "Brazil"
        OTHER = "OTHER", "Other"

    class CaretStyle(models.TextChoices):
        LINE = "line", "Line"
        BLOCK = "block", "Block"
        UNDERLINE = "underline", "Underline"
        OUTLINE = "outline", "Outline"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # Display
    display_name = models.CharField(max_length=50, blank=True, default="")
    bio = models.TextField(max_length=500, blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    country = models.CharField(
        max_length=10,
        choices=Country.choices,
        blank=True,
        default="",
    )

    # Typing Statistics (denormalized for fast access)
    total_tests = models.PositiveIntegerField(default=0)
    total_time_typing = models.PositiveIntegerField(default=0, help_text="Total seconds spent typing")
    best_wpm = models.FloatField(default=0.0)
    avg_wpm = models.FloatField(default=0.0)
    avg_accuracy = models.FloatField(default=0.0)

    # Progression
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    streak_days = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)

    # Preferences (JSON)
    preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="User preferences: theme, font, caret style, sounds, etc.",
    )

    # Active Theme
    active_theme = models.ForeignKey(
        "themes.Theme",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="active_users",
    )

    class Meta:
        db_table = "user_profiles"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"Profile: {self.user.username}"

    @property
    def default_preferences(self):
        """Default preference values."""
        return {
            "caret_style": self.CaretStyle.LINE,
            "smooth_caret": True,
            "sound_on_click": False,
            "sound_on_error": True,
            "show_live_wpm": True,
            "show_live_accuracy": True,
            "font_family": "Roboto Mono",
            "font_size": 18,
            "strict_space": False,
            "freedom_mode": False,
            "blind_mode": False,
        }

    def get_preference(self, key, default=None):
        """Get a preference value, falling back to defaults."""
        defaults = self.default_preferences
        return self.preferences.get(key, defaults.get(key, default))
