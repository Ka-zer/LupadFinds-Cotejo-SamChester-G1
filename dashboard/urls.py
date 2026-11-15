from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardRedirectView.as_view(), name="dashboard"),
    path("dashboard/student/", views.StudentDashboardView.as_view(), name="student_dashboard"),
    path("dashboard/staff/", views.StaffDashboardView.as_view(), name="staff_dashboard"),
    path("dashboard/admin/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
]