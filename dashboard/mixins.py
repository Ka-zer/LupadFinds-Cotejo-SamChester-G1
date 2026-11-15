from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Logged out -> login page. Logged in with the wrong role -> 403 Forbidden."""
    allowed_roles = []

    def test_func(self):
        return self.request.user.role in self.allowed_roles