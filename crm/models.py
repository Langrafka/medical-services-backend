from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import DecimalField, F, Sum

from operations.models import Nurse, Region
from web_content.models import Service


class FormStatus(models.TextChoices):
    NEW = "new", "New"
    PENDING = "pending", "Pending"
    DONE = "done", "Done"


class OrderStatus(models.TextChoices):
    NEW = "new", "New"
    PENDING = "pending", "Pending"
    DONE = "done", "Done"
    CANCELLED = "cancelled", "Cancelled"


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        related_name="addresses",
        blank=True,
        null=True,
    )
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=30)
    street = models.CharField(max_length=50, blank=True, null=True)
    building = models.CharField(max_length=30)
    local = models.CharField(max_length=30, blank=True, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="addresses"
    )

    def __str__(self):
        return f"{self.customer.last_name} {self.city}, {self.street} {self.building}"


class ContactForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(
        blank=True,
        null=True,
        validators=[
            MaxLengthValidator(limit_value=500, message="Description too long")
        ],
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="contact_forms",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=10, choices=FormStatus.choices, default=FormStatus.NEW
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"


class CareerForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    description = models.TextField(
        blank=True,
        null=True,
        validators=[
            MaxLengthValidator(limit_value=500, message="Description too long")
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=FormStatus.choices, default=FormStatus.NEW
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
    )
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="orders")
    nurse = models.ManyToManyField(Nurse, blank=True, related_name="orders")
    status = models.CharField(
        max_length=10, choices=OrderStatus.choices, default=OrderStatus.NEW
    )
    address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="orders", null=True, blank=True
    )
    scheduled = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_cost(self):
        if hasattr(self, "order_items"):
            result = self.order_items.aggregate(
                total=Sum(
                    F("price_at_buy") * F("quantity"),
                    output_field=DecimalField(),
                )
            )["total"]
            return result or 0
        return 0

    def __str__(self):
        customer_info = self.customer.phone if self.customer else "No customer"
        return f"Order #{self.pk} | {customer_info} | {self.status}"


class OrderItem(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, related_name="order_items"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_buy = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.price_at_buy:
            self.price_at_buy = self.service.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service.name} (x{self.quantity})"
