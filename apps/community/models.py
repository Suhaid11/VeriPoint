"""
Community App — Comment, Vote, BusinessResponse, Bookmark Models
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimestampedModel


class Comment(TimestampedModel):
    """Threaded comment on a review."""
    review = models.ForeignKey(
        'reviews.Review',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
    )
    body = models.TextField(max_length=2000)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'vp_comment'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['review', 'is_active']),
        ]

    def __str__(self):
        return f'Comment by {self.author.username} on review #{self.review_id}'

    @property
    def reply_count(self):
        return self.replies.filter(is_active=True).count()


class Vote(models.Model):
    """Upvote (+1) or downvote (−1) on a review."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='votes',
    )
    review = models.ForeignKey(
        'reviews.Review',
        on_delete=models.CASCADE,
        related_name='votes',
    )
    value = models.SmallIntegerField(
        choices=[(1, 'Upvote'), (-1, 'Downvote')],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vp_vote'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'review'],
                name='unique_vote_per_user_per_review',
            ),
        ]

    def __str__(self):
        direction = 'up' if self.value == 1 else 'down'
        return f'{self.user.username} voted {direction} on review #{self.review_id}'


class BusinessResponse(TimestampedModel):
    """Official business reply to a review."""
    review = models.OneToOneField(
        'reviews.Review',
        on_delete=models.CASCADE,
        related_name='business_response',
    )
    responder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business_responses',
    )
    body = models.TextField(max_length=5000)
    is_official = models.BooleanField(default=True)

    class Meta:
        db_table = 'vp_business_response'

    def __str__(self):
        return f'Response to review #{self.review_id}'


class Bookmark(models.Model):
    """User saves a business or review for later."""

    class BookmarkType(models.TextChoices):
        BUSINESS = 'business', 'Business'
        REVIEW = 'review', 'Review'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks',
    )
    business = models.ForeignKey(
        'businesses.Business',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bookmarks',
    )
    review = models.ForeignKey(
        'reviews.Review',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bookmarks',
    )
    bookmark_type = models.CharField(
        max_length=20,
        choices=BookmarkType.choices,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vp_bookmark'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'business'],
                condition=models.Q(business__isnull=False),
                name='unique_business_bookmark',
            ),
            models.UniqueConstraint(
                fields=['user', 'review'],
                condition=models.Q(review__isnull=False),
                name='unique_review_bookmark',
            ),
        ]

    def __str__(self):
        target = self.business or self.review
        return f'{self.user.username} bookmarked {target}'

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.business and not self.review:
            raise ValidationError('A bookmark must reference a business or review.')
        if self.business and self.review:
            raise ValidationError('A bookmark cannot reference both a business and a review.')
