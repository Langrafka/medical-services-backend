# crm/urls.py

from django.urls import path

from crm.views import (
    AddressAutocomplete,
    CareerFormView,
    ContactFormView,
    NurseAutocomplete,
)

urlpatterns = [
    path("contact_form/", ContactFormView.as_view(), name="contact_form"),
    path("career_form/", CareerFormView.as_view(), name="career_form"),
    path("nurse_autocomplete/", NurseAutocomplete.as_view(), name="nurse_autocomplete"),
    path(
        "address_autocomplete/",
        AddressAutocomplete.as_view(),
        name="address_autocomplete",
    ),
]
app_name = "crm"
