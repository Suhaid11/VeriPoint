"""Community — URL Configuration"""
from django.urls import path
from apps.community import views
from apps.community import views_verification

app_name = 'community'

urlpatterns = [
    path('vote/<int:pk>/', views.vote_view, name='vote'),
    path('comment/<int:pk>/', views.comment_view, name='comment'),
    path('respond/<int:pk>/', views.business_response_view, name='business_response'),
    path('bookmark/', views.toggle_bookmark_view, name='toggle_bookmark'),
    path('bookmarks/', views.BookmarkListView.as_view(), name='bookmarks'),
    path('verify-evidence/<int:pk>/', views_verification.verify_evidence_view, name='verify_evidence'),
]
