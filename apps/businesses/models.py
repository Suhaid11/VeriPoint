"""
Businesses App — Category, Business, BusinessPhoto Models
"""
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from apps.core.models import TimestampedModel


class Category(models.Model):
    """Hierarchical business category with optional parent."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Lucide icon name')
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'vp_category'
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['display_order', 'name']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def business_count(self):
        return self.businesses.filter(is_active=True).count()


class Business(TimestampedModel):
    """Core business listing."""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='businesses',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='businesses',
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    hours = models.JSONField(default=dict, blank=True)
    is_verified = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'vp_business'
        verbose_name_plural = 'Businesses'
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['city', 'is_active']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            n = 1
            while Business.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def primary_photo(self):
        return self.photos.filter(is_primary=True).first()

    @property
    def review_count(self):
        return self.reviews.filter(is_active=True).count()

    @property
    def avg_rating(self):
        from django.db.models import Avg
        result = self.reviews.filter(is_active=True).aggregate(avg=Avg('rating'))
        return round(result['avg'] or 0, 1)

    @property
    def avg_trust_score(self):
        from django.db.models import Avg
        result = self.reviews.filter(
            is_active=True, trust_score__isnull=False
        ).aggregate(avg=Avg('trust_score__total_score'))
        return round(result['avg'] or 0)


class BusinessPhoto(models.Model):
    """Gallery photo for a business."""
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='photos',
    )
    image = models.ImageField(upload_to='business_photos/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vp_business_photo'
        ordering = ['-is_primary', '-uploaded_at']

    def __str__(self):
        return f'Photo for {self.business.name}'
