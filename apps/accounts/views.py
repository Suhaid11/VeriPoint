"""
Accounts — Views for auth, profile, settings, dashboard.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.contrib import messages
from django.views.generic import DetailView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Avg, Count, Sum, Q

from apps.accounts.models import User, UserProfile
from apps.accounts.forms import RegisterForm, LoginForm, ProfileForm, SettingsForm
from apps.reviews.models import Review
from apps.businesses.models import Business


def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to VeriPoint, {user.first_name}!')
            return redirect('accounts:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'accounts:dashboard')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('core:landing')


class DashboardView(LoginRequiredMixin, TemplateView):
    """Authenticated user dashboard."""
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # User stats
        context['review_count'] = Review.objects.filter(
            author=user, is_active=True
        ).count()
        context['recent_reviews'] = Review.objects.filter(
            author=user, is_active=True
        ).select_related('business').prefetch_related(
            'trust_score', 'evidence_items'
        ).order_by('-created_at')[:5]

        # Reputation
        try:
            context['reputation'] = user.reputation
        except Exception:
            context['reputation'] = None

        # Business owner stats
        if user.is_business_owner:
            context['owned_businesses'] = Business.objects.filter(
                owner=user, is_active=True
            ).select_related('category')

        # Recent notifications
        context['recent_notifications'] = user.notifications.filter(
            is_read=False
        ).select_related('actor')[:5]

        return context


class ProfileView(DetailView):
    """Public user profile page."""
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object
        context['reviews'] = Review.objects.filter(
            author=profile_user, is_active=True
        ).select_related('business').prefetch_related(
            'trust_score', 'evidence_items'
        ).order_by('-created_at')[:10]
        try:
            context['reputation'] = profile_user.reputation
        except Exception:
            context['reputation'] = None
        return context


@login_required
def edit_profile_view(request):
    """Edit profile information."""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Update User fields
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.save(update_fields=['first_name', 'last_name'])
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile', username=request.user.username)
    else:
        form = ProfileForm(
            instance=profile,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        )
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def settings_view(request):
    """User settings / preferences."""
    profile = request.user.profile

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings saved.')
            return redirect('accounts:settings')
    else:
        form = SettingsForm(instance=profile)
    return render(request, 'accounts/settings.html', {'form': form})


# Password reset views using Django's built-in
class VPPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'emails/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class VPPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class VPPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class VPPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
