"""
Reviews App — Credibility Score Calculation Engine

Computes a 0–100 trust score from five weighted components:
  Evidence (40) + Reputation (20) + Community (20) + Recency (10) + Engagement (10)
"""
from django.conf import settings
from django.utils import timezone
from apps.reviews.models import TrustScore


def calculate_trust_score(review):
    """
    Calculate or update the TrustScore for a given review.
    Returns the TrustScore instance.
    """
    weights = settings.TRUST_SCORE_WEIGHTS

    # --- Evidence Score (0–40) ---
    evidence_items = review.evidence_items.all()
    evidence_count = evidence_items.count()
    # Bonus for type diversity
    type_diversity = evidence_items.values('evidence_type').distinct().count()
    evidence_score = min(
        weights['evidence_max'],
        (evidence_count * weights['evidence_per_item']) + (type_diversity * 3)
    )

    # --- Reputation Score (0–20) ---
    try:
        author_rep = review.author.reputation.score
    except Exception:
        author_rep = 0
    # Scale author reputation (0–500+) to 0–20
    reputation_score = min(
        weights['reputation_max'],
        int((author_rep / 500) * weights['reputation_max'])
    )

    # --- Community Score (0–20) ---
    vote_total = review.vote_score
    community_score = max(0, min(
        weights['community_max'],
        vote_total * weights['community_per_vote']
    ))

    # --- Recency Score (0–10) ---
    days_old = (timezone.now() - review.created_at).days
    decay_days = weights['recency_decay_days']
    if days_old <= 0:
        recency_score = weights['recency_max']
    elif days_old >= decay_days:
        recency_score = 0
    else:
        recency_score = int(
            weights['recency_max'] * (1 - (days_old / decay_days))
        )

    # --- Engagement Score (0–10) ---
    engagement_score = 0
    if review.comments.filter(is_active=True).exists():
        engagement_score += weights['engagement_comment_pts']
    if review.has_business_response:
        engagement_score += weights['engagement_response_pts']
    engagement_score = min(weights['engagement_max'], engagement_score)

    # --- Total ---
    total = evidence_score + reputation_score + community_score + recency_score + engagement_score

    # Create or update
    trust_score, _ = TrustScore.objects.update_or_create(
        review=review,
        defaults={
            'evidence_score': evidence_score,
            'reputation_score': reputation_score,
            'community_score': community_score,
            'recency_score': recency_score,
            'engagement_score': engagement_score,
            'total_score': total,
        },
    )
    return trust_score
