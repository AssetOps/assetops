from rest_framework import serializers

from .models import (
    Category,
    Location,
    InventoryItem,
    StockMovement,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class InventoryItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    location_name = serializers.CharField(
        source="location.name",
        read_only=True,
    )

    class Meta:
        model = InventoryItem

        fields = [
            "id",
            "name",
            "serial_number",
            "category",
            "category_name",
            "location",
            "location_name",
            "quantity",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class StockMovementSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(
        source="item.name",
        read_only=True,
    )

    class Meta:
        model = StockMovement

        fields = [
            "id",
            "item",
            "item_name",
            "movement_type",
            "quantity",
            "note",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "quantity",
            "created_at",
            "updated_at",
        ]