"""
Notifications App — Notification Model
"""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """User notification with generic targeting."""

    class NotificationType(models.TextChoices):
        REVIEW = 'review', 'New Review'
        COMMENT = 'comment', 'New Comment'
        VOTE = 'vote', 'New Vote'
        RESPONSE = 'response', 'Business Response'
        VERIFICATION = 'verification', 'Evidence Verified'
        SYSTEM = 'system', 'System'

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actions',
    )
    verb = models.CharField(max_length=100)
    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        db_index=True,
    )
    target_type = models.CharField(max_length=50, blank=True)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'vp_notification'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at']),
        ]

    def __str__(self):
        actor_name = self.actor.username if self.actor else 'System'
        return f'{actor_name} {self.verb}'
