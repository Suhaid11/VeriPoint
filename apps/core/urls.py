"""Core — URL Configuration"""
from django.urls import path
from apps.core import views

app_name = 'core'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('features/', views.FeaturesView.as_view(), name='features'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('help/', views.HelpView.as_view(), name='help'),
]
