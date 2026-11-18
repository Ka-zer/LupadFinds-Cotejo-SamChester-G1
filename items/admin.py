from django.contrib import admin
from .models import Category, ItemReport, Location


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(ItemReport)
class ItemReportAdmin(admin.ModelAdmin):
    list_display = ["item_name", "report_type", "category", "location",
                    "user", "status", "item_date"]
    list_filter = ["report_type", "status", "category"]
    search_fields = ["item_name", "description"]