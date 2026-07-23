"""
Reviews App — Review, Evidence, EvidenceVerification, TrustScore Models
"""
import os
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from apps.core.models import TimestampedModel


def validate_evidence_file(value):
    """Validate evidence file extension and size."""
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in settings.ALLOWED_EVIDENCE_EXTENSIONS:
        raise ValidationError(
            f'File type "{ext}" not allowed. '
            f'Allowed: {", ".join(settings.ALLOWED_EVIDENCE_EXTENSIONS)}'
        )
    if value.size > settings.MAX_EVIDENCE_FILE_SIZE:
        max_mb = settings.MAX_EVIDENCE_FILE_SIZE // (1024 * 1024)
        raise ValidationError(f'File size exceeds {max_mb} MB limit.')


class Review(TimestampedModel):
    """Evidence-based review — the heart of VeriPoint."""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    business = models.ForeignKey(
        'businesses.Business',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    visit_date = models.DateField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='1–5 rating (secondary to trust score)',
    )
    is_edited = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'vp_review'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'business'],
                name='unique_review_per_user_per_business',
            ),
        ]
        indexes = [
            models.Index(fields=['business', 'is_active', '-created_at']),
            models.Index(fields=['author', 'is_active']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f'{self.title} — {self.author.username}'

    @property
    def evidence_count(self):
        return self.evidence_items.count()

    @property
    def vote_score(self):
        from django.db.models import Sum
        result = self.votes.aggregate(total=Sum('value'))
        return result['total'] or 0

    @property
    def upvote_count(self):
        return self.votes.filter(value=1).count()

    @property
    def downvote_count(self):
        return self.votes.filter(value=-1).count()

    @property
    def comment_count(self):
        return self.comments.filter(is_active=True).count()

    @property
    def has_business_response(self):
        return hasattr(self, 'business_response') and self.business_response is not None


class Evidence(models.Model):
    """File attachment proving a review claim."""

    class EvidenceType(models.TextChoices):
        PHOTO = 'photo', 'Photo'
        INVOICE = 'invoice', 'Invoice'
        RECEIPT = 'receipt', 'Receipt'
        DOCUMENT = 'document', 'Document'
        SCREENSHOT = 'screenshot', 'Screenshot'

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='evidence_items',
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_evidence',
    )
    file = models.FileField(
        upload_to='evidence/%Y/%m/',
        validators=[validate_evidence_file],
    )
    evidence_type = models.CharField(
        max_length=20,
        choices=EvidenceType.choices,
        db_index=True,
    )
    caption = models.CharField(max_length=300, blank=True)
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(help_text='Size in bytes')
    is_verified = models.BooleanField(default=False, db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'vp_evidence'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.get_evidence_type_display()}: {self.original_filename}'

    @property
    def file_size_display(self):
        """Human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB']:
            if size < 1024:
                return f'{size:.1f} {unit}'
            size /= 1024
        return f'{size:.1f} GB'

    @property
    def is_image(self):
        ext = os.path.splitext(self.original_filename)[1].lower()
        return ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']

    @property
    def verification_count(self):
        return self.verifications.count()

    @property
    def authentic_count(self):
        return self.verifications.filter(status='authentic').count()


class EvidenceVerification(models.Model):
    """Community verification of evidence authenticity."""

    class Status(models.TextChoices):
        AUTHENTIC = 'authentic', 'Authentic'
        SUSPICIOUS = 'suspicious', 'Suspicious'
        INCONCLUSIVE = 'inconclusive', 'Inconclusive'

    evidence = models.ForeignKey(
        Evidence,
        on_delete=models.CASCADE,
        related_name='verifications',
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='evidence_verifications',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        db_index=True,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vp_evidence_verification'
        constraints = [
            models.UniqueConstraint(
                fields=['evidence', 'verified_by'],
                name='unique_verification_per_user',
            ),
        ]

    def __str__(self):
        return f'{self.verified_by.username}: {self.get_status_display()}'


class TrustScore(models.Model):
    """Calculated credibility score for a review (0–100)."""
    review = models.OneToOneField(
        Review,
        on_delete=models.CASCADE,
        related_name='trust_score',
    )
    evidence_score = models.PositiveSmallIntegerField(default=0)
    reputation_score = models.PositiveSmallIntegerField(default=0)
    community_score = models.PositiveSmallIntegerField(default=0)
    recency_score = models.PositiveSmallIntegerField(default=0)
    engagement_score = models.PositiveSmallIntegerField(default=0)
    total_score = models.PositiveSmallIntegerField(default=0, db_index=True)
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vp_trust_score'

    def __str__(self):
        return f'Trust: {self.total_score}/100 for review #{self.review_id}'
