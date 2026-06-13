"""
Results — Models
=================
"""

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Result(TimeStampedModel):
    """
    Stores the result of a completed typing test.
    """

    class Mode(models.TextChoices):
        TIME = "time", "Time"
        WORDS = "words", "Words"
        QUOTE = "quote", "Quote"
        CUSTOM = "custom", "Custom"
        CODE = "code", "Code"

    # User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="results",
        db_index=True,
    )

    # Performance Metrics
    wpm = models.FloatField(help_text="Net Words Per Minute")
    raw_wpm = models.FloatField(help_text="Raw WPM (no error penalty)")
    accuracy = models.FloatField(help_text="Accuracy percentage (0-100)")
    consistency = models.FloatField(help_text="Consistency score (0-100)")

    # Test Configuration
    mode = models.CharField(max_length=20, choices=Mode.choices)
    duration = models.PositiveIntegerField(help_text="Test duration in seconds")
    language = models.CharField(max_length=20, default="en")

    # Character Breakdown
    characters_typed = models.PositiveIntegerField(default=0)
    correct_chars = models.PositiveIntegerField(default=0)
    incorrect_chars = models.PositiveIntegerField(default=0)
    extra_chars = models.PositiveIntegerField(default=0)
    missed_chars = models.PositiveIntegerField(default=0)

    # Detailed Data (JSON)
    keystrokes = models.JSONField(
        default=list,
        blank=True,
        help_text="Keystroke timing data",
    )
    char_log = models.JSONField(
        default=list,
        blank=True,
        help_text="Character-by-character log",
    )
    wpm_history = models.JSONField(
        default=list,
        blank=True,
        help_text="WPM at each second",
    )

    # Personal Best
    is_personal_best = models.BooleanField(default=False)

    # Anti-Cheat
    is_flagged = models.BooleanField(
        default=False,
        help_text="Flagged by anti-cheat system",
    )
    flag_reasons = models.JSONField(
        default=list,
        blank=True,
        help_text="Reasons for flagging",
    )

    # Word List Reference
    wordlist = models.ForeignKey(
        "wordlists.WordList",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="results",
    )

    class Meta:
        db_table = "results"
        verbose_name = "Result"
        verbose_name_plural = "Results"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["user", "mode", "-wpm"]),
            models.Index(fields=["mode", "-wpm"]),
            models.Index(fields=["-wpm"]),
            models.Index(fields=["language", "-wpm"]),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.wpm} WPM ({self.mode})"

    def save(self, *args, **kwargs):
        # Check if this is a personal best
        if not self.is_flagged:
            existing_best = (
                Result.objects.filter(
                    user=self.user,
                    mode=self.mode,
                    duration=self.duration,
                    language=self.language,
                    is_flagged=False,
                )
                .exclude(pk=self.pk)
                .order_by("-wpm")
                .first()
            )
            if existing_best is None or self.wpm > existing_best.wpm:
                self.is_personal_best = True
                # Unmark previous PB
                if existing_best:
                    Result.objects.filter(pk=existing_best.pk).update(is_personal_best=False)

        super().save(*args, **kwargs)
