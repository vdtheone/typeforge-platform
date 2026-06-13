"""
Core Models — Shared Base Models
=================================
"""

import uuid

from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    `created_at` and `updated_at` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class UUIDModel(models.Model):
    """
    Abstract base model that uses UUID as primary key.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(UUIDModel, TimeStampedModel):
    """
    Abstract base model combining UUID primary key with timestamps.
    """

    class Meta(UUIDModel.Meta, TimeStampedModel.Meta):
        abstract = True
