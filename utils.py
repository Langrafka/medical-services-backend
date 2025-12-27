# utils.py
import phonenumbers
from phonenumbers import NumberParseException
from rest_framework.exceptions import ValidationError


def _phone_validator(obj, value):
    try:
        parsed_number = phonenumbers.parse(value, "UA")
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError("Phone number is not valid for UA")
        return phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )
    except NumberParseException:
        raise ValidationError("Invalid phone number format")
