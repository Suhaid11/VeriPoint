"""Businesses — URL Configuration"""
from django.urls import path
from apps.businesses import views

app_name = 'businesses'

urlpatterns = [
    path('', views.BusinessListView.as_view(), name='list'),
    path('create/', views.create_business_view, name='create'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('<slug:slug>/', views.BusinessDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', views.edit_business_view, name='edit'),
]
