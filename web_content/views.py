# web_content/views.py

from rest_framework.generics import ListAPIView
from rest_framework.throttling import ScopedRateThrottle

from web_content.models import ServiceType
from web_content.serializers import ServiceTypeSerializer


class ServiceView(ListAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "services_throttle"
    serializer_class = ServiceTypeSerializer
    queryset = ServiceType.objects.all().select_related("services")
