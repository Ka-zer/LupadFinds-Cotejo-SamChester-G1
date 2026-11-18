from django.urls import path
from . import views

urlpatterns = [
    path("lost/", views.LostReportListView.as_view(), name="lost_list"),
    path("lost/new/", views.LostReportCreateView.as_view(), name="lost_create"),
    path("lost/<int:pk>/", views.LostReportDetailView.as_view(), name="lost_detail"),
    path("lost/<int:pk>/edit/", views.LostReportUpdateView.as_view(), name="lost_update"),
    path("lost/<int:pk>/delete/", views.LostReportDeleteView.as_view(), name="lost_delete"),
]