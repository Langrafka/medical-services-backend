# web_content/serializers.py

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from web_content.models import Service, ServiceType


class ServiceSerializer(ModelSerializer):
    service_type = serializers.CharField(source="service_type.name", read_only=True)

    class Meta:
        model = Service
        fields = [
            "name_en",
            "name_uk",
            "price",
            "description_en",
            "description_uk",
        ]


class ServiceTypeSerializer(ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceType
        fields = ["name_en", "name_uk", "services"]
