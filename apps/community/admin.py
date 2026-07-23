"""Community — Admin Registration"""
from django.contrib import admin
from apps.community.models import Comment, Vote, BusinessResponse, Bookmark


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'review', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['body', 'author__username']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'value', 'created_at']
    list_filter = ['value', 'created_at']


@admin.register(BusinessResponse)
class BusinessResponseAdmin(admin.ModelAdmin):
    list_display = ['responder', 'review', 'is_official', 'created_at']
    list_filter = ['is_official', 'created_at']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'bookmark_type', 'business', 'review', 'created_at']
    list_filter = ['bookmark_type', 'created_at']
