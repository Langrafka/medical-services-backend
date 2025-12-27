from django.urls import path

from web_content.views import ServiceView

urlpatterns = [path("services/", ServiceView.as_view(), name="services")]

app_name = "web_content"
