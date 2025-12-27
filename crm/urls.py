# crm/urls.py

from django.urls import path
from rest_framework.urls import app_name

from crm.views import CareerFormCreate, ContactFormCreate

urlpatterns = [
    path("contact_form/", ContactFormCreate.as_view(), name="contact_form"),
    path("career_form/", CareerFormCreate.as_view(), name="career_form"),
]
app_name = "crm"
