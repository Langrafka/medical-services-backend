# crm/urls.py

from django.urls import path


from crm.views import CareerFormView, ContactFormView

urlpatterns = [
    path("contact_form/", ContactFormView.as_view(), name="contact_form"),
    path("career_form/", CareerFormView.as_view(), name="career_form"),

]
app_name = "crm"
