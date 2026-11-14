from django.conf import settings
from django.core.exceptions import ValidationError


def validate_school_email(value):
    """Only allow emails from the school domains listed in settings."""
    domain = value.rsplit("@", 1)[-1].lower()
    if domain not in settings.ALLOWED_EMAIL_DOMAINS:
        allowed = ", ".join("@" + d for d in settings.ALLOWED_EMAIL_DOMAINS)
        raise ValidationError(f"Please use your school email ({allowed}).")