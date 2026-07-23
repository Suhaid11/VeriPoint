"""
Moderation App — AuditLog, ActivityLog Models
"""
from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """Tracks administrative and moderation actions."""

    class Action(models.TextChoices):
        CREATE = 'create', 'Create'
        UPDATE = 'update', 'Update'
        DELETE = 'delete', 'Delete'
        MODERATE = 'moderate', 'Moderate'
        VERIFY = 'verify', 'Verify'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
    )
    action = models.CharField(
        max_length=50,
        choices=Action.choices,
        db_index=True,
    )
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'vp_audit_log'
        ordering = ['-created_at']

    def __str__(self):
        user_name = self.user.username if self.user else 'System'
        return f'{user_name} {self.action} {self.model_name} #{self.object_id}'


class ActivityLog(models.Model):
    """Tracks user activity for analytics."""

    class ActionType(models.TextChoices):
        LOGIN = 'login', 'Login'
        REVIEW = 'review', 'Review'
        VOTE = 'vote', 'Vote'
        COMMENT = 'comment', 'Comment'
        SEARCH = 'search', 'Search'
        VIEW = 'view', 'View'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activity_logs',
    )
    action_type = models.CharField(
        max_length=50,
        choices=ActionType.choices,
        db_index=True,
    )
    description = models.CharField(max_length=300, blank=True)
    target_type = models.CharField(max_length=50, blank=True)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'vp_activity_log'
        ordering = ['-created_at']

    def __str__(self):
        user_name = self.user.username if self.user else 'Anonymous'
        return f'{user_name}: {self.action_type}'
