"""
Community — Evidence Verification Endpoint
"""
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

from apps.reviews.models import Evidence, EvidenceVerification
from apps.reviews.scoring import calculate_trust_score


@login_required
@require_POST
def verify_evidence_view(request, pk):
    """
    Community member submits an evidence authenticity check.
    Status choices: authentic, suspicious, inconclusive.
    """
    evidence = get_object_or_404(Evidence, pk=pk)

    # Can't verify own uploaded evidence
    if evidence.uploaded_by == request.user:
        return JsonResponse({'error': 'You cannot verify your own evidence.'}, status=403)

    status = request.POST.get('status', '').strip()
    notes = request.POST.get('notes', '').strip()

    if status not in ['authentic', 'suspicious', 'inconclusive']:
        return JsonResponse({'error': 'Invalid status choice.'}, status=400)

    verification, created = EvidenceVerification.objects.update_or_create(
        evidence=evidence,
        verified_by=request.user,
        defaults={
            'status': status,
            'notes': notes,
        }
    )

    # Update evidence verified boolean if majority authentic
    authentic_count = evidence.verifications.filter(status='authentic').count()
    if authentic_count >= 2:
        evidence.is_verified = True
        evidence.save(update_fields=['is_verified'])

    # Update verifier's reputation score
    rep = request.user.reputation
    rep.total_verifications += 1
    rep.recalculate()

    # Recalculate review trust score
    calculate_trust_score(evidence.review)

    return JsonResponse({
        'status': 'ok',
        'verification_status': verification.status,
        'authentic_count': authentic_count,
        'is_verified': evidence.is_verified,
    })
