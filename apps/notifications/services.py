"""
Notifications App — Service helpers for creating notifications.
"""
from apps.notifications.models import Notification


def notify(recipient, actor, verb, notification_type, target_type='', target_id=None):
    """
    Create a notification. Skips if recipient == actor.
    """
    if recipient == actor:
        return None
    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        notification_type=notification_type,
        target_type=target_type,
        target_id=target_id,
    )


def notify_new_review(review):
    """Notify business owner about a new review."""
    if review.business.owner and review.business.owner != review.author:
        notify(
            recipient=review.business.owner,
            actor=review.author,
            verb=f'reviewed your business "{review.business.name}"',
            notification_type='review',
            target_type='review',
            target_id=review.pk,
        )


def notify_new_comment(comment):
    """Notify review author about a new comment."""
    notify(
        recipient=comment.review.author,
        actor=comment.author,
        verb=f'commented on your review "{comment.review.title}"',
        notification_type='comment',
        target_type='review',
        target_id=comment.review.pk,
    )
    # Also notify parent comment author if it's a reply
    if comment.parent and comment.parent.author != comment.author:
        notify(
            recipient=comment.parent.author,
            actor=comment.author,
            verb='replied to your comment',
            notification_type='comment',
            target_type='review',
            target_id=comment.review.pk,
        )


def notify_new_vote(vote):
    """Notify review author about a vote."""
    direction = 'upvoted' if vote.value == 1 else 'downvoted'
    notify(
        recipient=vote.review.author,
        actor=vote.user,
        verb=f'{direction} your review "{vote.review.title}"',
        notification_type='vote',
        target_type='review',
        target_id=vote.review.pk,
    )


def notify_business_response(response):
    """Notify review author that the business responded."""
    notify(
        recipient=response.review.author,
        actor=response.responder,
        verb=f'responded to your review of "{response.review.business.name}"',
        notification_type='response',
        target_type='review',
        target_id=response.review.pk,
    )
