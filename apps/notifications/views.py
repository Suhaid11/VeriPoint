"""
Notifications — Views for listing and managing notifications.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.conf import settings

from apps.notifications.models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    """User notification feed."""
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = settings.NOTIFICATIONS_PER_PAGE

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related('actor')


@login_required
@require_POST
def mark_read_view(request, pk):
    """Mark a single notification as read."""
    Notification.objects.filter(
        pk=pk, recipient=request.user
    ).update(is_read=True)
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def mark_all_read_view(request):
    """Mark all notifications as read."""
    Notification.objects.filter(
        recipient=request.user, is_read=False
    ).update(is_read=True)
    return JsonResponse({'status': 'ok'})
