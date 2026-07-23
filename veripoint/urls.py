"""
VeriPoint — Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path('django-admin/', admin.site.urls),

    # VeriPoint apps
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('businesses/', include('apps.businesses.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('community/', include('apps.community.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('admin-dashboard/', include('apps.moderation.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'apps.core.views.custom_404'
handler500 = 'apps.core.views.custom_500'
