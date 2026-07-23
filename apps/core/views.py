"""
Core — Views for static pages (landing, about, features, contact, help)
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from apps.businesses.models import Business, Category
from apps.reviews.models import Review


class LandingPageView(TemplateView):
    """Public landing page with featured content."""
    template_name = 'core/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(
            is_active=True, parent__isnull=True
        ).order_by('display_order')[:8]
        context['featured_businesses'] = Business.objects.filter(
            is_active=True
        ).select_related('category').order_by('-created_at')[:6]
        context['recent_reviews'] = Review.objects.filter(
            is_active=True
        ).select_related(
            'author', 'business'
        ).prefetch_related('evidence_items').order_by('-created_at')[:4]
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'


class FeaturesView(TemplateView):
    template_name = 'core/features.html'


class ContactView(TemplateView):
    template_name = 'core/contact.html'


class HelpView(TemplateView):
    template_name = 'core/help.html'


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    return render(request, 'errors/500.html', status=500)
