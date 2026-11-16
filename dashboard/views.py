from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView

from accounts.models import CustomUser
from .mixins import RoleRequiredMixin

Role = CustomUser.Role

# Which dashboard each role goes to
ROLE_HOME = {
    Role.STUDENT: "student_dashboard",
    Role.STAFF: "staff_dashboard",
    Role.ADMIN: "admin_dashboard",
}


class DashboardRedirectView(LoginRequiredMixin, RedirectView):
    """Sends each logged-in user to the dashboard for their role."""
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse(ROLE_HOME[self.request.user.role])


class StudentDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/student.html"
    allowed_roles = [Role.STUDENT]


class StaffDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/staff.html"
    allowed_roles = [Role.STAFF]


class AdminDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/admin.html"
    allowed_roles = [Role.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = CustomUser.objects
        context["total_users"] = users.count()
        context["student_count"] = users.filter(role=Role.STUDENT).count()
        context["staff_count"] = users.filter(role=Role.STAFF).count()
        context["recent_users"] = users.order_by("-date_joined")[:5]
        return context