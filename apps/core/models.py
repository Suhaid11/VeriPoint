"""
Core App — Abstract Base Models & Shared Utilities

Provides TimestampedModel and common validators reused across all apps.
"""
from django.db import models


class TimestampedModel(models.Model):
    """Abstract base with created_at and updated_at timestamps."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
