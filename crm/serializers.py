# crm/serializers.py
from rest_framework.serializers import ModelSerializer

from crm.models import CareerForm, ContactForm
from utils import _phone_validator


class ContactFormSerializer(ModelSerializer):
    class Meta:
        model = ContactForm
        fields = ["first_name", "last_name", "phone", "description"]

    def validate_phone(self, value):
        return _phone_validator(self, value)


class CareerFormSerializer(ModelSerializer):
    class Meta:
        model = CareerForm
        fields = ["first_name", "last_name", "phone", "description"]

    def validate_phone(self, value):
        return _phone_validator(self, value)
