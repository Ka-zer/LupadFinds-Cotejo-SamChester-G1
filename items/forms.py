from django import forms
from django.utils import timezone

from .models import ItemReport


class LostReportForm(forms.ModelForm):
    class Meta:
        model = ItemReport
        fields = ("item_name", "category", "location", "item_date", "description")
        labels = {
            "item_name": "Item name",
            "location": "Last known location",
            "item_date": "Date lost",
        }
        widgets = {
            "item_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Color, brand, size, marks, contents..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "-- Select a category --"
        self.fields["location"].empty_label = "-- Select a location --"
        # The date picker can't go past today
        self.fields["item_date"].widget.attrs["max"] = timezone.localdate().isoformat()

    def clean_item_name(self):
        name = self.cleaned_data["item_name"].strip()
        if len(name) < 3:
            raise forms.ValidationError("Item name must be at least 3 characters.")
        return name

    def clean_item_date(self):                       # BR-07
        date = self.cleaned_data["item_date"]
        if date > timezone.localdate():
            raise forms.ValidationError("The date lost cannot be in the future.")
        return date

    def clean_description(self):                     # BR-06
        text = self.cleaned_data["description"].strip()
        if len(text) < 10:
            raise forms.ValidationError(
                "Please describe the item in at least 10 characters.")
        return text