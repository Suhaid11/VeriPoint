"""
Businesses — Forms for creating and editing businesses.
"""
from django import forms
from apps.businesses.models import Business, BusinessPhoto


class BusinessForm(forms.ModelForm):
    """Create or edit a business listing."""

    class Meta:
        model = Business
        fields = [
            'name', 'category', 'short_description', 'description',
            'address', 'city', 'state', 'zip_code',
            'phone', 'email', 'website',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Business name'}),
            'short_description': forms.TextInput(attrs={'placeholder': 'Brief tagline (300 chars max)'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe this business...'}),
            'address': forms.TextInput(attrs={'placeholder': 'Street address'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State / Province'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'ZIP / Postal code'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1 (555) 000-0000'}),
            'email': forms.EmailInput(attrs={'placeholder': 'contact@business.com'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://business.com'}),
        }


class BusinessPhotoForm(forms.ModelForm):
    """Upload a business photo."""

    class Meta:
        model = BusinessPhoto
        fields = ['image', 'caption', 'is_primary']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Photo caption (optional)'}),
        }
