"""
Reviews — Forms for creating reviews and uploading evidence.
"""
from django import forms
from apps.reviews.models import Review, Evidence


class ReviewForm(forms.ModelForm):
    """Create or edit a review."""

    class Meta:
        model = Review
        fields = ['title', 'body', 'visit_date', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Summarize your experience'}),
            'body': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Share the details of your experience. '
                               'What happened? What did you observe?',
            }),
            'visit_date': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'When did you visit?',
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1, 'max': 5, 'step': 1,
            }),
        }


class EvidenceForm(forms.ModelForm):
    """Upload evidence for a review."""

    class Meta:
        model = Evidence
        fields = ['file', 'evidence_type', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'What does this evidence show?'}),
        }
