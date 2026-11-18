from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.models import CustomUser
from .forms import LostReportForm
from .models import ItemReport

Role = CustomUser.Role
LOST = ItemReport.ReportType.LOST


class LostReportQuerysetMixin(LoginRequiredMixin):
    """Admins see every lost report; other users only see their own."""

    def get_queryset(self):
        reports = ItemReport.objects.filter(report_type=LOST)
        if self.request.user.role != Role.ADMIN:
            reports = reports.filter(user=self.request.user)
        return reports.select_related("category", "location", "user")


class LostReportListView(LostReportQuerysetMixin, ListView):
    template_name = "items/lost_list.html"
    context_object_name = "reports"


class LostReportDetailView(LostReportQuerysetMixin, DetailView):
    template_name = "items/lost_detail.html"
    context_object_name = "report"


class LostReportCreateView(LoginRequiredMixin, CreateView):
    model = ItemReport
    form_class = LostReportForm
    template_name = "items/lost_forms.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.report_type = LOST
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("lost_detail", args=[self.object.pk])


class LostReportUpdateView(LostReportQuerysetMixin, UpdateView):
    model = ItemReport
    form_class = LostReportForm
    template_name = "items/lost_forms.html"

    def get_success_url(self):
        return reverse("lost_detail", args=[self.object.pk])


class LostReportDeleteView(LostReportQuerysetMixin, DeleteView):
    model = ItemReport
    template_name = "items/lost_confirm_delete.html"
    context_object_name = "report"

    def get_success_url(self):
        return reverse("lost_list")
