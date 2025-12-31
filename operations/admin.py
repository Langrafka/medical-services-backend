from django.contrib import admin

from operations.models import Nurse, Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
        "telegram_id",
        "email",
    )
    search_fields = (
        "first_name",
        "last_name",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("region")
