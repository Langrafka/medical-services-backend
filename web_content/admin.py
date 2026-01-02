from django.contrib import admin

from web_content.models import Service, ServiceType


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "service_type",
        "price",
    )
    list_select_related = ("service_type",)
    search_fields = (
        "name",
        "service_type__name",
        "price",
    )
    autocomplete_fields = ("service_type",)
