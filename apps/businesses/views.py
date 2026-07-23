"""
Businesses — Views for listing, search, detail, create, edit.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg, Count

from apps.businesses.models import Business, Category
from apps.businesses.forms import BusinessForm, BusinessPhotoForm
from apps.reviews.models import Review


class BusinessListView(ListView):
    """Browse all businesses with search and filters."""
    model = Business
    template_name = 'businesses/business_list.html'
    context_object_name = 'businesses'
    paginate_by = 12

    def get_queryset(self):
        qs = Business.objects.filter(
            is_active=True
        ).select_related('category', 'owner').annotate(
            review_count_val=Count('reviews', filter=Q(reviews__is_active=True)),
            avg_rating_val=Avg('reviews__rating', filter=Q(reviews__is_active=True)),
        )

        # Search
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(city__icontains=q) | Q(description__icontains=q)
            )

        # Category filter
        category_slug = self.request.GET.get('category', '')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        # City filter
        city = self.request.GET.get('city', '').strip()
        if city:
            qs = qs.filter(city__icontains=city)

        # Verified only
        if self.request.GET.get('verified') == '1':
            qs = qs.filter(is_verified=True)

        # Sort
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'rating':
            qs = qs.order_by('-avg_rating_val', '-created_at')
        elif sort == 'reviews':
            qs = qs.order_by('-review_count_val', '-created_at')
        elif sort == 'name':
            qs = qs.order_by('name')
        else:
            qs = qs.order_by('-created_at')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(
            is_active=True, parent__isnull=True
        ).order_by('display_order')
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_city'] = self.request.GET.get('city', '')
        context['selected_sort'] = self.request.GET.get('sort', 'newest')
        return context


class BusinessDetailView(DetailView):
    """Business profile page with reviews."""
    model = Business
    template_name = 'businesses/business_detail.html'
    context_object_name = 'business'

    def get_queryset(self):
        return Business.objects.filter(
            is_active=True
        ).select_related('category', 'owner')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = self.object

        context['reviews'] = Review.objects.filter(
            business=business, is_active=True
        ).select_related(
            'author__profile', 'trust_score'
        ).prefetch_related(
            'evidence_items', 'votes', 'comments'
        ).order_by('-created_at')

        context['photos'] = business.photos.all()

        # Check if current user can review
        if self.request.user.is_authenticated:
            context['user_has_reviewed'] = Review.objects.filter(
                author=self.request.user, business=business
            ).exists()
            context['is_bookmarked'] = business.bookmarks.filter(
                user=self.request.user
            ).exists()
        return context


class CategoryListView(ListView):
    """Browse businesses by category."""
    model = Category
    template_name = 'businesses/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(
            is_active=True, parent__isnull=True
        ).prefetch_related('children').order_by('display_order')


class CategoryDetailView(DetailView):
    """Businesses within a specific category."""
    model = Category
    template_name = 'businesses/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['businesses'] = Business.objects.filter(
            category=self.object, is_active=True
        ).select_related('category').annotate(
            review_count_val=Count('reviews', filter=Q(reviews__is_active=True)),
            avg_rating_val=Avg('reviews__rating', filter=Q(reviews__is_active=True)),
        ).order_by('-created_at')
        return context


@login_required
def create_business_view(request):
    """Create a new business listing."""
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            # Update user role to business owner if not already
            if request.user.role == 'reviewer':
                request.user.role = 'business_owner'
                request.user.save(update_fields=['role'])
            messages.success(request, f'"{business.name}" has been created.')
            return redirect('businesses:detail', slug=business.slug)
    else:
        form = BusinessForm()
    return render(request, 'businesses/business_form.html', {'form': form, 'editing': False})


@login_required
def edit_business_view(request, slug):
    """Edit an existing business."""
    business = get_object_or_404(Business, slug=slug, is_active=True)

    # Only owner or admin can edit
    if business.owner != request.user and not request.user.is_platform_admin:
        messages.error(request, 'You do not have permission to edit this business.')
        return redirect('businesses:detail', slug=slug)

    if request.method == 'POST':
        form = BusinessForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, 'Business updated successfully.')
            return redirect('businesses:detail', slug=business.slug)
    else:
        form = BusinessForm(instance=business)
    return render(request, 'businesses/business_form.html', {
        'form': form, 'business': business, 'editing': True,
    })
