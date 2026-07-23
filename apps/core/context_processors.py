"""
Core — Context Processors

Injects site-wide data into every template context.
"""
from django.conf import settings


def site_context(request):
    """Add site info and unread notification count to all templates."""
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TAGLINE': settings.SITE_TAGLINE,
        'SITE_DESCRIPTION': settings.SITE_DESCRIPTION,
    }
    if request.user.is_authenticated:
        context['unread_notification_count'] = (
            request.user.notifications.filter(is_read=False).count()
        )
    return context
