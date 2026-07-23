"""Moderation — Admin Registration"""
from django.contrib import admin
from apps.moderation.models import AuditLog, ActivityLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_id', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['model_name', 'user__username', 'ip_address']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'changes', 'ip_address', 'created_at']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'description', 'created_at']
    list_filter = ['action_type', 'created_at']
    search_fields = ['description', 'user__username']
    readonly_fields = ['user', 'action_type', 'description', 'target_type', 'target_id', 'metadata', 'created_at']
