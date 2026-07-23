"""
Community — Views for voting, commenting, bookmarks, business responses.
"""
import json
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from apps.community.models import Comment, Vote, BusinessResponse, Bookmark
from apps.reviews.models import Review
from apps.reviews.scoring import calculate_trust_score
from apps.notifications.services import (
    notify_new_comment, notify_new_vote, notify_business_response,
)


@login_required
@require_POST
def vote_view(request, pk):
    """Upvote or downvote a review."""
    review = get_object_or_404(Review, pk=pk, is_active=True)
    value = int(request.POST.get('value', 0))

    if value not in (1, -1):
        return JsonResponse({'error': 'Invalid vote value'}, status=400)

    # Can't vote on own review
    if review.author == request.user:
        return JsonResponse({'error': 'Cannot vote on own review'}, status=403)

    vote, created = Vote.objects.get_or_create(
        user=request.user,
        review=review,
        defaults={'value': value},
    )

    if not created:
        if vote.value == value:
            # Toggle off — remove vote
            vote.delete()
            action = 'removed'
        else:
            # Change vote direction
            vote.value = value
            vote.save(update_fields=['value'])
            action = 'changed'
    else:
        action = 'created'
        notify_new_vote(vote)

    # Recalculate trust score
    calculate_trust_score(review)

    return JsonResponse({
        'action': action,
        'vote_score': review.vote_score,
        'upvotes': review.upvote_count,
        'downvotes': review.downvote_count,
    })


@login_required
@require_POST
def comment_view(request, pk):
    """Add a comment to a review."""
    review = get_object_or_404(Review, pk=pk, is_active=True)
    body = request.POST.get('body', '').strip()

    if not body:
        messages.error(request, 'Comment cannot be empty.')
        return redirect('reviews:detail', pk=pk)

    parent_id = request.POST.get('parent_id')
    parent = None
    if parent_id:
        parent = Comment.objects.filter(pk=parent_id, review=review).first()

    comment = Comment.objects.create(
        review=review,
        author=request.user,
        parent=parent,
        body=body,
    )

    # Recalculate trust score (engagement component)
    calculate_trust_score(review)

    # Notify
    notify_new_comment(comment)

    messages.success(request, 'Comment posted.')
    return redirect('reviews:detail', pk=pk)


@login_required
@require_POST
def business_response_view(request, pk):
    """Business owner responds to a review."""
    review = get_object_or_404(Review, pk=pk, is_active=True)

    # Only business owner or admin can respond
    if review.business.owner != request.user and not request.user.is_platform_admin:
        messages.error(request, 'Only the business owner can respond.')
        return redirect('reviews:detail', pk=pk)

    # Check if already responded
    if hasattr(review, 'business_response'):
        messages.warning(request, 'A response already exists for this review.')
        return redirect('reviews:detail', pk=pk)

    body = request.POST.get('body', '').strip()
    if not body:
        messages.error(request, 'Response cannot be empty.')
        return redirect('reviews:detail', pk=pk)

    response = BusinessResponse.objects.create(
        review=review,
        responder=request.user,
        body=body,
    )

    calculate_trust_score(review)
    notify_business_response(response)

    messages.success(request, 'Business response posted.')
    return redirect('reviews:detail', pk=pk)


@login_required
@require_POST
def toggle_bookmark_view(request):
    """Toggle bookmark on a business or review."""
    bookmark_type = request.POST.get('type', '')
    target_id = request.POST.get('id', '')

    if bookmark_type == 'business':
        from apps.businesses.models import Business
        obj = get_object_or_404(Business, pk=target_id)
        bm, created = Bookmark.objects.get_or_create(
            user=request.user,
            business=obj,
            defaults={'bookmark_type': 'business'},
        )
    elif bookmark_type == 'review':
        obj = get_object_or_404(Review, pk=target_id)
        bm, created = Bookmark.objects.get_or_create(
            user=request.user,
            review=obj,
            defaults={'bookmark_type': 'review'},
        )
    else:
        return JsonResponse({'error': 'Invalid type'}, status=400)

    if not created:
        bm.delete()
        return JsonResponse({'bookmarked': False})

    return JsonResponse({'bookmarked': True})


class BookmarkListView(LoginRequiredMixin, ListView):
    """User's saved bookmarks."""
    template_name = 'community/bookmarks.html'
    context_object_name = 'bookmarks'
    paginate_by = 20

    def get_queryset(self):
        return Bookmark.objects.filter(
            user=self.request.user
        ).select_related('business__category', 'review__business').order_by('-created_at')
