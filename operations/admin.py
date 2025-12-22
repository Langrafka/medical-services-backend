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
