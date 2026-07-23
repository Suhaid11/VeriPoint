"""
Accounts App — Signals

Creates UserProfile and Reputation when a new User is created.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_and_reputation(sender, instance, created, **kwargs):
    """Auto-create profile and reputation for new users."""
    if created:
        from apps.accounts.models import UserProfile, Reputation
        UserProfile.objects.create(user=instance)
        Reputation.objects.create(user=instance)
