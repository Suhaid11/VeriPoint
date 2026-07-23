"""
Core — Reusable View Mixins
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Ensure the logged-in user is the owner of the object."""

    def test_func(self):
        obj = self.get_object()
        # Check common owner field names
        if hasattr(obj, 'author'):
            return obj.author == self.request.user
        if hasattr(obj, 'owner'):
            return obj.owner == self.request.user
        if hasattr(obj, 'user'):
            return obj.user == self.request.user
        return False


class ModeratorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Ensure the logged-in user is a moderator or admin."""

    def test_func(self):
        return self.request.user.is_moderator


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Ensure the logged-in user is a platform admin."""

    def test_func(self):
        return self.request.user.is_platform_admin
