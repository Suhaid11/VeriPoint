"""Businesses — Admin Registration"""
from django.contrib import admin
from apps.businesses.models import Category, Business, BusinessPhoto


class BusinessPhotoInline(admin.TabularInline):
    model = BusinessPhoto
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'display_order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'city', 'owner', 'is_verified', 'is_active', 'created_at']
    list_filter = ['is_verified', 'is_active', 'category', 'city']
    search_fields = ['name', 'city', 'description', 'address']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BusinessPhotoInline]
