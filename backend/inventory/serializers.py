from decimal import Decimal

from rest_framework import serializers

from .models import Category, Location, Product, StockLevel, StockMovement


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "sku",
            "category",
            "category_name",
        )


class StockLevelSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    location_name = serializers.CharField(
        source="location.name",
        read_only=True,
    )

    class Meta:
        model = StockLevel
        fields = (
            "id",
            "product",
            "product_name",
            "location",
            "location_name",
            "quantity_on_hand",
            "last_updated",
        )

        read_only_fields = (
            "id",
            "quantity_on_hand",
            "last_updated",
        )


class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    location_name = serializers.CharField(
        source="location.name",
        read_only=True,
    )

    class Meta:
        model = StockMovement
        fields = (
            "id",
            "product",
            "product_name",
            "location",
            "location_name",
            "reception",
            "sale",
            "quantity",
            "reason",
            "created_at",
            "synced_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "synced_at",
        )


class StockChangeSerializer(serializers.Serializer):
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
    )

    quantity = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )

    reason = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
    )


class StockAdjustmentSerializer(serializers.Serializer):
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
    )

    quantity = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal(0),
    )

    reason = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
    )