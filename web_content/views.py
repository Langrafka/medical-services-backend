# web_content/views.py

from rest_framework.generics import ListAPIView

from web_content.models import Service
from web_content.serializers import ServiceSerializer


class ServiceView(ListAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all().select_related("service_type")
