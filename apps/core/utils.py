"""
Core — Utility functions shared across apps.
"""
import os
from django.utils.text import slugify


def get_client_ip(request):
    """Extract client IP from request, handling proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def unique_slugify(instance, value, slug_field='slug'):
    """Generate a unique slug for a model instance."""
    model = instance.__class__
    base_slug = slugify(value)
    slug = base_slug
    n = 1
    while model.objects.filter(**{slug_field: slug}).exclude(pk=instance.pk).exists():
        slug = f'{base_slug}-{n}'
        n += 1
    return slug


def safe_filename(filename):
    """Sanitize a filename for safe storage."""
    name, ext = os.path.splitext(filename)
    safe_name = slugify(name) or 'file'
    return f'{safe_name}{ext.lower()}'
