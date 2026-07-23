"""
Reviews — Views for creating, viewing, and managing reviews and evidence.
"""
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.generic import DetailView, ListView

from apps.reviews.models import Review, Evidence
from apps.reviews.forms import ReviewForm, EvidenceForm
from apps.reviews.scoring import calculate_trust_score
from apps.businesses.models import Business
from apps.notifications.services import notify_new_review


class ReviewDetailView(DetailView):
    """Full review detail with evidence and comments."""
    model = Review
    template_name = 'reviews/review_detail.html'
    context_object_name = 'review'

    def get_queryset(self):
        return Review.objects.filter(
            is_active=True
        ).select_related(
            'author__profile', 'author__reputation',
            'business', 'trust_score',
        ).prefetch_related(
            'evidence_items',
            'comments__author__profile',
            'votes',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.object
        if self.request.user.is_authenticated:
            user_vote = review.votes.filter(user=self.request.user).first()
            context['user_vote'] = user_vote.value if user_vote else 0
            context['is_bookmarked'] = review.bookmarks.filter(
                user=self.request.user
            ).exists()
        # Business response
        try:
            context['business_response'] = review.business_response
        except Exception:
            context['business_response'] = None
        return context


@login_required
def create_review_view(request, slug):
    """Create a new review for a business."""
    business = get_object_or_404(Business, slug=slug, is_active=True)

    # Check if user already reviewed
    if Review.objects.filter(author=request.user, business=business).exists():
        messages.warning(request, 'You have already reviewed this business.')
        return redirect('businesses:detail', slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        files = request.FILES.getlist('evidence_files')

        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.business = business
            review.save()

            # Handle evidence uploads
            evidence_types = request.POST.getlist('evidence_types')
            evidence_captions = request.POST.getlist('evidence_captions')

            for i, f in enumerate(files[:settings.MAX_EVIDENCE_PER_REVIEW]):
                ext = os.path.splitext(f.name)[1].lower()
                if ext not in settings.ALLOWED_EVIDENCE_EXTENSIONS:
                    continue
                if f.size > settings.MAX_EVIDENCE_FILE_SIZE:
                    continue

                e_type = evidence_types[i] if i < len(evidence_types) else 'photo'
                caption = evidence_captions[i] if i < len(evidence_captions) else ''

                Evidence.objects.create(
                    review=review,
                    uploaded_by=request.user,
                    file=f,
                    evidence_type=e_type,
                    caption=caption,
                    original_filename=f.name,
                    file_size=f.size,
                )

            # Calculate trust score
            calculate_trust_score(review)

            # Update author reputation
            rep = request.user.reputation
            rep.total_reviews += 1
            rep.total_evidence += len(files)
            rep.recalculate()

            # Notify business owner
            notify_new_review(review)

            messages.success(request, 'Your review has been published!')
            return redirect('reviews:detail', pk=review.pk)
    else:
        form = ReviewForm()

    return render(request, 'reviews/review_form.html', {
        'form': form,
        'business': business,
    })


@login_required
def add_evidence_view(request, pk):
    """Add more evidence to an existing review."""
    review = get_object_or_404(Review, pk=pk, author=request.user, is_active=True)

    if request.method == 'POST':
        files = request.FILES.getlist('evidence_files')
        current_count = review.evidence_items.count()
        remaining = settings.MAX_EVIDENCE_PER_REVIEW - current_count

        if remaining <= 0:
            messages.warning(request, 'Maximum evidence limit reached.')
            return redirect('reviews:detail', pk=pk)

        evidence_types = request.POST.getlist('evidence_types')
        evidence_captions = request.POST.getlist('evidence_captions')

        added = 0
        for i, f in enumerate(files[:remaining]):
            ext = os.path.splitext(f.name)[1].lower()
            if ext not in settings.ALLOWED_EVIDENCE_EXTENSIONS:
                continue
            if f.size > settings.MAX_EVIDENCE_FILE_SIZE:
                continue

            e_type = evidence_types[i] if i < len(evidence_types) else 'photo'
            caption = evidence_captions[i] if i < len(evidence_captions) else ''

            Evidence.objects.create(
                review=review,
                uploaded_by=request.user,
                file=f,
                evidence_type=e_type,
                caption=caption,
                original_filename=f.name,
                file_size=f.size,
            )
            added += 1

        if added:
            calculate_trust_score(review)
            messages.success(request, f'{added} evidence item(s) added.')
        return redirect('reviews:detail', pk=pk)

    return render(request, 'reviews/add_evidence.html', {'review': review})


class LeaderboardView(ListView):
    """Top reviewers by reputation score."""
    template_name = 'reviews/leaderboard.html'
    context_object_name = 'top_reviewers'

    def get_queryset(self):
        from apps.accounts.models import Reputation
        return Reputation.objects.select_related(
            'user__profile'
        ).order_by('-score')[:settings.LEADERBOARD_SIZE]
