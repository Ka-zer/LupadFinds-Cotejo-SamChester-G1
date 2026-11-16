from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser
from .validators import validate_school_email


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="School email",
        validators=[validate_school_email],
    )
    # ADMIN is left out so nobody can make themselves an admin
    role = forms.ChoiceField(
        label="I am a",
        choices=[c for c in CustomUser.Role.choices
                 if c[0] != CustomUser.Role.ADMIN],
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "first_name", "last_name",
                  "email", "contact_number", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "contact_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        # Superusers (admins) may use a non-school email
        if not self.instance.is_superuser:
            validate_school_email(email)
        # Email must stay unique, ignoring the user's own record
        if CustomUser.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email