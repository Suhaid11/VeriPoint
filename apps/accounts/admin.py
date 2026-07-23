"""Accounts — Admin Registration"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.accounts.models import User, UserProfile, Reputation


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class ReputationInline(admin.StackedInline):
    model = Reputation
    can_delete = False
    readonly_fields = ['score', 'level']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [UserProfileInline, ReputationInline]
    fieldsets = BaseUserAdmin.fieldsets + (
        ('VeriPoint', {'fields': ('role',)}),
    )
