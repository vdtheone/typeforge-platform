"""
Word Lists — Models
====================
"""

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Language(TimeStampedModel):
    """Supported languages for typing tests."""

    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        help_text="ISO language code (e.g., 'en', 'es', 'fr')",
    )
    is_active = models.BooleanField(default=True)
    flag_emoji = models.CharField(max_length=10, blank=True, default="")

    class Meta:
        db_table = "languages"
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        ordering = ["name"]

    def __str__(self):
        return f"{self.flag_emoji} {self.name}" if self.flag_emoji else self.name


class WordList(TimeStampedModel):
    """
    Word list for typing tests.
    Each word list contains a JSON array of words.
    """

    class Difficulty(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"
        EXPERT = "expert", "Expert"

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    description = models.TextField(blank=True, default="")

    # Content
    words = models.JSONField(
        default=list,
        help_text="JSON array of words",
    )
    word_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of words in the list (auto-calculated)",
    )

    # Classification
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="word_lists",
    )
    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
    )

    # Ownership
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="word_lists",
    )

    # Visibility
    is_public = models.BooleanField(default=True)
    is_default = models.BooleanField(
        default=False,
        help_text="Whether this is a built-in default word list",
    )

    # Stats
    times_used = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "word_lists"
        verbose_name = "Word List"
        verbose_name_plural = "Word Lists"
        ordering = ["-is_default", "name"]
        indexes = [
            models.Index(fields=["language", "difficulty"]),
            models.Index(fields=["is_public", "is_default"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.language.code})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if isinstance(self.words, list):
            self.word_count = len(self.words)
        super().save(*args, **kwargs)


class Quote(TimeStampedModel):
    """Curated quotes for quote typing mode."""

    text = models.TextField()
    source = models.CharField(max_length=200, blank=True, default="")
    author = models.CharField(max_length=100, blank=True, default="")

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="quotes",
    )

    word_count = models.PositiveIntegerField(default=0)
    char_count = models.PositiveIntegerField(default=0)

    class Difficulty(models.TextChoices):
        SHORT = "short", "Short (< 50 words)"
        MEDIUM = "medium", "Medium (50–100 words)"
        LONG = "long", "Long (100+ words)"

    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "quotes"
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ["-created_at"]

    def __str__(self):
        return f'"{self.text[:50]}..." — {self.author or "Unknown"}'

    def save(self, *args, **kwargs):
        self.word_count = len(self.text.split())
        self.char_count = len(self.text)
        super().save(*args, **kwargs)
