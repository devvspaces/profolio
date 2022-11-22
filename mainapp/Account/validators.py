import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone(phone=''):
    pattern = r'[\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})' # noqa
    s = re.match(pattern, phone)
    if s is None:
        raise ValidationError(_('Provide a valid phone number'),)
