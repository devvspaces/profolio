from Account.validators import validate_phone
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.parametrize(
    "phone",
    [
        "08012345678",
        "080-123-4567",
        "080 123 4567",
        "080.123.4567",
        "0801234567",
        "080-123-45678",
    ]
)
def test_validate_phone(phone):
    assert validate_phone(phone) is None


def test_validate_phone_error():
    with pytest.raises(ValidationError):
        validate_phone("+08012345678")
