# crm/views.py
from dal import autocomplete
from rest_framework.generics import CreateAPIView
from rest_framework.throttling import ScopedRateThrottle

from crm.models import Address, Customer
from crm.serializers import CareerFormSerializer, ContactFormSerializer
from operations.models import Nurse


class ContactFormView(CreateAPIView):
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "forms_throttle"
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
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "forms_throttle"
    serializer_class = CareerFormSerializer


class NurseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Nurse.objects.all()
        qs = Nurse.objects.all()
        region = self.forwarded.get("region", None)
        if region:
            qs = qs.filter(region=region)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class AddressAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Address.objects.all()
        qs = Address.objects.all()
        region = self.forwarded.get("region", None)
        if region:
            qs = qs.filter(region=region)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
