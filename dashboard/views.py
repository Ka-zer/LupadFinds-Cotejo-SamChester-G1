from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    """Protected page. Logged-out users are sent to the login page.
    Replaced by the role-based dashboards in the next feature."""
    template_name = "dashboard/home.html"