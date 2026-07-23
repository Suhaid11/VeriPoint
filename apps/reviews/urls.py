"""Reviews — URL Configuration"""
from django.urls import path
from apps.reviews import views

app_name = 'reviews'

urlpatterns = [
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='detail'),
    path('create/<slug:slug>/', views.create_review_view, name='create'),
    path('<int:pk>/add-evidence/', views.add_evidence_view, name='add_evidence'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
]
