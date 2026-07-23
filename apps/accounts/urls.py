"""Accounts — URL Configuration"""
from django.urls import path
from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),

    # Password reset
    path('password-reset/', views.VPPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.VPPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.VPPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.VPPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
