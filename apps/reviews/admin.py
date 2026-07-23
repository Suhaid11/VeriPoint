"""Reviews — Admin Registration"""
from django.contrib import admin
from apps.reviews.models import Review, Evidence, EvidenceVerification, TrustScore


class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 0
    readonly_fields = ['original_filename', 'file_size', 'uploaded_at']


class TrustScoreInline(admin.StackedInline):
    model = TrustScore
    readonly_fields = ['total_score', 'evidence_score', 'reputation_score', 'community_score', 'recency_score', 'engagement_score', 'calculated_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'business', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['title', 'body', 'author__username', 'business__name']
    inlines = [EvidenceInline, TrustScoreInline]


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'evidence_type', 'review', 'uploaded_by', 'is_verified', 'uploaded_at']
    list_filter = ['evidence_type', 'is_verified', 'uploaded_at']
    search_fields = ['original_filename', 'caption', 'uploaded_by__username']


@admin.register(EvidenceVerification)
class EvidenceVerificationAdmin(admin.ModelAdmin):
    list_display = ['evidence', 'verified_by', 'status', 'created_at']
    list_filter = ['status', 'created_at']


@admin.register(TrustScore)
class TrustScoreAdmin(admin.ModelAdmin):
    list_display = ['review', 'total_score', 'calculated_at']
    readonly_fields = ['total_score', 'evidence_score', 'reputation_score', 'community_score', 'recency_score', 'engagement_score', 'calculated_at']
