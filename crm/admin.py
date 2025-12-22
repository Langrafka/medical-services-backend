from django.contrib import admin

from .models import CareerForm, ContactForm, Order, OrderItem, Address, Customer


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


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "order",
        "quantity",
        "price_at_buy",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "region",
        "status",
        "description",
        "created_at",
        "updated_at",
        "calculated_total",
    )


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
