"""
Accounts App — User, UserProfile, Reputation Models
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    """Extended user model with role-based access."""

    class Role(models.TextChoices):
        REVIEWER = 'reviewer', 'Reviewer'
        BUSINESS_OWNER = 'business_owner', 'Business Owner'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.REVIEWER,
        db_index=True,
    )

    class Meta:
        db_table = 'vp_user'
        indexes = [
            models.Index(fields=['date_joined']),
        ]

    def __str__(self):
        return self.username

    @property
    def is_business_owner(self):
        return self.role == self.Role.BUSINESS_OWNER

    @property
    def is_moderator(self):
        return self.role in (self.Role.MODERATOR, self.Role.ADMIN)

    @property
    def is_platform_admin(self):
        return self.role == self.Role.ADMIN


class UserProfile(models.Model):
    """Extended profile: avatar, bio, preferences."""

    class ThemeChoice(models.TextChoices):
        LIGHT = 'light', 'Light'
        DARK = 'dark', 'Dark'
        SYSTEM = 'system', 'System'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    theme_preference = models.CharField(
        max_length=10,
        choices=ThemeChoice.choices,
        default=ThemeChoice.SYSTEM,
    )
    email_notifications = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vp_user_profile'

    def __str__(self):
        return f'{self.user.username} profile'

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None


class Reputation(models.Model):
    """Aggregated reviewer reputation score."""

    class Level(models.TextChoices):
        NEWCOMER = 'newcomer', 'Newcomer'
        CONTRIBUTOR = 'contributor', 'Contributor'
        TRUSTED = 'trusted', 'Trusted'
        EXPERT = 'expert', 'Expert'
        AUTHORITY = 'authority', 'Authority'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reputation',
    )
    total_reviews = models.PositiveIntegerField(default=0)
    total_evidence = models.PositiveIntegerField(default=0)
    total_verifications = models.PositiveIntegerField(default=0)
    total_helpful_votes = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0, db_index=True)
    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.NEWCOMER,
        db_index=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vp_reputation'
        ordering = ['-score']

    def __str__(self):
        return f'{self.user.username}: {self.score} ({self.get_level_display()})'

    def recalculate(self):
        """Recalculate score from component counts and update level."""
        self.score = (
            (self.total_reviews * 10)
            + (self.total_evidence * 5)
            + (self.total_verifications * 15)
            + (self.total_helpful_votes * 3)
        )
        # Determine level
        for level_name, (low, high) in settings.REPUTATION_LEVELS.items():
            if low <= self.score <= high:
                self.level = level_name
                break
        self.save(update_fields=['score', 'level', 'updated_at'])
