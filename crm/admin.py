from django.contrib import admin
from django.db.models import DecimalField, F, Sum
from django.urls import reverse
from django.utils.html import format_html

from operations.models import Nurse

from .models import Address, CareerForm, ContactForm, Customer, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price_at_buy",)


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


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

    readonly_fields = ("create_order_link",)

    def create_order_link(self, obj):
        if obj.customer:
            url = reverse("admin:crm_order_add")
            params = f"customer={obj.customer.id}&description=From contact form"

            # If customer has only one address add in into URL.
            if obj.customer.addresses.count() == 1:
                address_id = obj.customer.addresses.first().id
                params += f"&address={address_id}"

            full_url = f"{url}?{params}"
            return format_html(
                '<a class="button" style="background: #417690; color: white; padding: 5px 10px; border-radius: 4px;" href="{}">Quick Order</a>',
                full_url,
            )
        return "Assign customer first"

    create_order_link.short_description = "Action"


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
    autocomplete_fields = ["customer", "address", "nurse"]

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "address":
            order_id = request.resolver_match.kwargs.get("object_id")
            if order_id:
                order = self.get_object(request, order_id)
                if order and order.customer:
                    kwargs["queryset"] = Address.objects.filter(customer=order.customer)
                else:
                    kwargs["queryset"] = Address.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.address and obj.address.region:
            obj.region = obj.address.region
        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "nurse":
            order_id = request.resolver_match.kwargs.get("object_id")
            if order_id:
                order = self.get_object(request, order_id)
                if order and order.region:
                    kwargs["queryset"] = Nurse.objects.filter(region=order.region)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


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
    search_fields = (
        "city",
        "street",
        "customer__last_name",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("region", "customer")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
        "created_at",
        "updated_at",
    )
    inlines = [
        AddressInline,
    ]
    search_fields = (
        "first_name",
        "last_name",
        "phone",
    )
