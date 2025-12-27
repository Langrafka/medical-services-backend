# crm/views.py

from rest_framework.generics import CreateAPIView

from crm.models import Customer
from crm.serializers import CareerFormSerializer, ContactFormSerializer


class ContactFormView(CreateAPIView):
    serializer_class = ContactFormSerializer

    def perform_create(self, serializer):
        phone = serializer.validated_data.get("phone")
        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name")

        customer, created = Customer.objects.get_or_create(
            phone=phone,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
            },
        )

        serializer.save(customer=customer)


class CareerFormView(CreateAPIView):
    serializer_class = CareerFormSerializer
