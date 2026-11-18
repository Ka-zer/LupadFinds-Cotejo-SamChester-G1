from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView

from accounts.models import CustomUser
from items.models import ItemReport
from .mixins import RoleRequiredMixin

Role = CustomUser.Role
LOST = ItemReport.ReportType.LOST

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


class MemberDashboardView(RoleRequiredMixin, TemplateView):
    """Shared by Student and Staff: shows the user's OWN lost reports."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mine = ItemReport.objects.filter(user=self.request.user, report_type=LOST)
        context["my_lost_count"] = mine.count()
        context["my_open_count"] = mine.filter(status=ItemReport.Status.OPEN).count()
        context["recent_reports"] = mine.select_related("category", "location")[:5]
        return context


class StudentDashboardView(MemberDashboardView):
    template_name = "dashboard/student.html"
    allowed_roles = [Role.STUDENT]


class StaffDashboardView(MemberDashboardView):
    template_name = "dashboard/staff.html"
    allowed_roles = [Role.STAFF]


class AdminDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/admin.html"
    allowed_roles = [Role.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = CustomUser.objects
        lost = ItemReport.objects.filter(report_type=LOST)
        context["total_users"] = users.count()
        context["student_count"] = users.filter(role=Role.STUDENT).count()
        context["staff_count"] = users.filter(role=Role.STAFF).count()
        context["total_lost"] = lost.count()
        context["open_lost"] = lost.filter(status=ItemReport.Status.OPEN).count()
        context["recent_lost"] = lost.select_related("category", "location", "user")[:5]
        return context