"""Moderation — URL Configuration"""
from django.urls import path
from apps.moderation import views

app_name = 'moderation'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    path('audit-log/', views.AuditLogListView.as_view(), name='audit_log'),
    path('users/', views.UserManagementView.as_view(), name='user_list'),
]
