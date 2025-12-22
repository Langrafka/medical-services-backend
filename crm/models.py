from django.db import models

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
        related_name="addressees",
        blank=True,
        null=True,
    )
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=30)
    street = models.CharField(max_length=50, blank=True, null=True)
    building = models.CharField(max_length=30)
    local = models.CharField(max_length=30, blank=True, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="addressees"
    )

    def __str__(self):
        return f"{self.street} {self.building} {self.local} {self.city}"


class ContactForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="contact_forms"
    )
    status = models.CharField(
        max_length=10, choices=FormStatus.choices, default=FormStatus.NEW
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"

    def get_or_create(self):
        customer = Customer.objects.get(self.phone)
        if customer:
            return customer
        return Customer(self)


class CareerForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
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
    quantity = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=OrderStatus.choices, default=OrderStatus.NEW
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    @property
    def calculated_total(self):
        if hasattr(self, "order_items"):
            return sum(
                item.price_at_buy * item.quantity for item in self.order_items.all()
            )
        return 0

    def __str__(self):
        return f"Phone: {self.customer.phone} Status: {self.status}"


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
