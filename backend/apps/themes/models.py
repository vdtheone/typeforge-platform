"""
Themes — Models
================
"""

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Theme(TimeStampedModel):
    """
    Theme configuration storing CSS variables as JSON.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    description = models.TextField(blank=True, default="")

    # CSS Variables stored as JSON
    css_variables = models.JSONField(
        default=dict,
        help_text="CSS custom properties (e.g., --bg-color, --text-color, --caret-color)",
    )

    # Preview
    preview_image = models.ImageField(
        upload_to="theme_previews/",
        blank=True,
        null=True,
    )

    # Ownership
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="themes",
    )

    # Visibility
    is_public = models.BooleanField(default=True)
    is_default = models.BooleanField(
        default=False,
        help_text="Built-in theme shipped with the platform",
    )

    # Social
    likes_count = models.PositiveIntegerField(default=0)
    usage_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "themes"
        verbose_name = "Theme"
        verbose_name_plural = "Themes"
        ordering = ["-is_default", "-likes_count"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ThemeLike(TimeStampedModel):
    """Tracks which users liked which themes."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="theme_likes",
    )
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        db_table = "theme_likes"
        unique_together = ("user", "theme")
        verbose_name = "Theme Like"
        verbose_name_plural = "Theme Likes"

    def __str__(self):
        return f"{self.user.username} likes {self.theme.name}"
