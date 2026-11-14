from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    # Temporary: back to the signup page so the success message shows.
    # In the login feature, change this to reverse_lazy("login").
    success_url = reverse_lazy("signup")
    success_message = "Account created successfully! You can now log in."

    def form_invalid(self, form):
        messages.error(self.request, "Please fix the errors below.")
        return super().form_invalid(form)