from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)          # BR-04

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)         # BR-04

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ItemReport(models.Model):
    class ReportType(models.TextChoices):
        LOST = "LOST", "Lost"
        FOUND = "FOUND", "Found"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        RETURNED = "RETURNED", "Returned"

    # Relationships from your ERD
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="item_reports")
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name="reports")
    location = models.ForeignKey(Location, on_delete=models.PROTECT,
                                 related_name="reports")

    report_type = models.CharField(max_length=5, choices=ReportType.choices,
                                   default=ReportType.LOST)       # BR-05
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    item_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices,
                              default=Status.OPEN)                # BR-08
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(report_type__in=["LOST", "FOUND"]),
                name="report_type_valid"),
            models.CheckConstraint(
                condition=models.Q(status__in=["OPEN", "RETURNED"]),
                name="report_status_valid"),
        ]

    def __str__(self):
        return f"{self.get_report_type_display()}: {self.item_name}"