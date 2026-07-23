"""
Moderation — Admin dashboard views, audit logs, platform stats.
"""
from django.views.generic import TemplateView, ListView
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

from apps.core.mixins import ModeratorRequiredMixin
from apps.accounts.models import User
from apps.businesses.models import Business
from apps.reviews.models import Review, Evidence
from apps.moderation.models import AuditLog, ActivityLog


class AdminDashboardView(ModeratorRequiredMixin, TemplateView):
    """Platform admin overview with key metrics."""
    template_name = 'moderation/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)

        context['total_users'] = User.objects.count()
        context['total_businesses'] = Business.objects.filter(is_active=True).count()
        context['total_reviews'] = Review.objects.filter(is_active=True).count()
        context['total_evidence'] = Evidence.objects.count()

        # 30-day trends
        context['new_users_30d'] = User.objects.filter(
            date_joined__gte=thirty_days_ago
        ).count()
        context['new_reviews_30d'] = Review.objects.filter(
            created_at__gte=thirty_days_ago, is_active=True
        ).count()
        context['new_businesses_30d'] = Business.objects.filter(
            created_at__gte=thirty_days_ago, is_active=True
        ).count()

        # Average trust score
        context['avg_trust_score'] = Review.objects.filter(
            is_active=True, trust_score__isnull=False
        ).aggregate(avg=Avg('trust_score__total_score'))['avg'] or 0

        # Recent audit log
        context['recent_audits'] = AuditLog.objects.select_related(
            'user'
        ).order_by('-created_at')[:10]

        return context


class AuditLogListView(ModeratorRequiredMixin, ListView):
    """Paginated audit log viewer."""
    model = AuditLog
    template_name = 'moderation/audit_log.html'
    context_object_name = 'audit_logs'
    paginate_by = 25

    def get_queryset(self):
        return AuditLog.objects.select_related('user').order_by('-created_at')


class UserManagementView(ModeratorRequiredMixin, ListView):
    """User listing for moderation."""
    model = User
    template_name = 'moderation/user_list.html'
    context_object_name = 'users'
    paginate_by = 25

    def get_queryset(self):
        qs = User.objects.select_related('profile', 'reputation').order_by('-date_joined')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(username__icontains=q) | Q(email__icontains=q)
            )
        return qs
