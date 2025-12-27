from django.contrib import admin
from django.db.models import DecimalField, F, Sum

from .models import Address, CareerForm, ContactForm, Customer, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price_at_buy",)


@admin.register(CareerForm)
class CareerFormAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
        "status",
    )


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
        "status",
    )


#
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = (
#         "service",
#         "order",
#         "quantity",
#         "price_at_buy",
#     )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "region",
        "address",
        "status",
        "description",
        "created_at",
        "updated_at",
        "get_total_cost",
    )
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _annotated_total=Sum(
                F("order_items__price_at_buy") * F("order_items__quantity"),
                output_field=DecimalField(),
            )
        )
        return queryset

    def get_total_cost(self, obj):
        """
        Check for result in annotate (for list),
        if not get it from model's property.
        """
        total = getattr(obj, "_annotated_total", obj.total_cost)
        return f"{total:.2f}"

    get_total_cost.short_description = "Total cost"
    get_total_cost.admin_order_field = "_annotated_total"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "region",
        "city",
        "postal_code",
        "street",
        "building",
        "local",
        "customer",
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
        "created_at",
        "updated_at",
    )
