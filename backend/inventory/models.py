import uuid
from typing import ClassVar

from django.db import models


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class StockLevel(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stock_levels"
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="stock_levels"
    )
    quantity_on_hand = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints: ClassVar[list] = [
            models.UniqueConstraint(
                fields=["product", "location"], name="unique_stock_per_location"
            )
        ]


class Reception(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="receptions"
    )
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name="receptions"
    )
    received_at = models.DateField()


class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name="sales"
    )
    sold_at = models.DateField()


class StockMovement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="movements"
    )
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name="movements"
    )
    reception = models.ForeignKey(
        Reception,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movements",
    )
    sale = models.ForeignKey(
        Sale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movements",
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    synced_at = models.DateTimeField(null=True, blank=True)
