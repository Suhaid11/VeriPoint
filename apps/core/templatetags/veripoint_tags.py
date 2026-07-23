"""
Core — Custom Template Tags & Filters
"""
from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def trust_score_color(score):
    """Return CSS class based on trust score value."""
    if score is None:
        return 'score-none'
    score = int(score)
    if score >= 80:
        return 'score-excellent'
    if score >= 60:
        return 'score-good'
    if score >= 40:
        return 'score-average'
    if score >= 20:
        return 'score-low'
    return 'score-poor'


@register.filter
def trust_score_label(score):
    """Return human-readable label for trust score."""
    if score is None:
        return 'Not Scored'
    score = int(score)
    if score >= 80:
        return 'Excellent'
    if score >= 60:
        return 'Good'
    if score >= 40:
        return 'Average'
    if score >= 20:
        return 'Low'
    return 'Poor'


@register.filter
def reputation_badge_color(level):
    """Return CSS class for reputation level badge."""
    colors = {
        'newcomer': 'badge-neutral',
        'contributor': 'badge-info',
        'trusted': 'badge-success',
        'expert': 'badge-warning',
        'authority': 'badge-primary',
    }
    return colors.get(level, 'badge-neutral')


@register.filter
def star_range(value):
    """Return range for star display. Usage: {% for i in rating|star_range %}"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


@register.filter
def empty_star_range(value):
    """Return range for empty stars. Usage: {% for i in rating|empty_star_range %}"""
    try:
        return range(5 - int(value))
    except (ValueError, TypeError):
        return range(5)


@register.filter
def short_timesince(value):
    """Short timesince: '2 days ago' instead of '2 days, 3 hours ago'."""
    try:
        ts = timesince(value)
        # Return only the first part
        return ts.split(',')[0] + ' ago'
    except Exception:
        return ''


@register.filter
def evidence_icon(evidence_type):
    """Return Lucide icon name for evidence type."""
    icons = {
        'photo': 'camera',
        'invoice': 'file-text',
        'receipt': 'receipt',
        'document': 'file',
        'screenshot': 'monitor',
    }
    return icons.get(evidence_type, 'file')


@register.simple_tag
def active_nav(request, url_name, *args):
    """Return 'active' class if current URL matches."""
    from django.urls import reverse, resolve
    try:
        current = resolve(request.path_info).url_name
        if current == url_name:
            return 'active'
        if current in args:
            return 'active'
    except Exception:
        pass
    return ''
