from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    radius = models.PositiveSmallIntegerField(blank=True, null=True)
    lat = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.name


class Nurse(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    telegram_id = models.BigIntegerField(unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    region = models.ManyToManyField(Region, blank=True, related_name="nurses")

    def __str__(self):
        regions = ", ".join([r.name for r in self.region.all()])
        return f"{self.first_name} {self.last_name} ({regions})"
