# web_content/serializers.py

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from web_content.models import Service


class ServiceSerializer(ModelSerializer):
    service_type = serializers.CharField(source="service_type.name", read_only=True)

    class Meta:
        model = Service
        fields = [
            "name",
            "service_type",
            "price",
            "description",
        ]
