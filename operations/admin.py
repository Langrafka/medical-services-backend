from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html_join

from operations.models import Nurse, Region


class NurseInline(admin.TabularInline):
    model = Nurse.region.through
    autocomplete_fields = ("nurse",)
    extra = 1
    verbose_name = "nurse"
    verbose_name_plural = "Assigned nurses"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("nurse")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_nurses_count",
    )
    fieldsets = (
        (None, {"fields": ("name",)}),
        (
            "Geolocation (Optional)",
            {
                "classes": ("collapse",),
                "fields": (
                    "radius",
                    "lat",
                    "lon",
                ),
            },
        ),
    )
    inlines = (NurseInline,)
    search_fields = ("name",)

    def display_nurses_count(self, obj):
        return obj.nurses_count

    display_nurses_count.short_description = "Amount of assigned nurses"
    display_nurses_count.admin_order_field = "nurses_count"

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(nurses_count=Count("nurses"))


@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
        "display_region_links",
    )
    search_fields = (
        "first_name",
        "last_name",
        "phone",
    )
    filter_horizontal = ("region",)

    list_filter = ("region",)

    def display_region_links(self, obj):
        region_data = (
            (reverse("admin:operations_region_change", args=[region.pk]), region.name)
            for region in obj.region.all()
        )

        return format_html_join(", ", '<a href="{}">{}</a>', region_data)

    display_region_links.short_description = "Assigned regions"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("region")
