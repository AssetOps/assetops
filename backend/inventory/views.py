from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Category,
    Location,
    InventoryItem,
    StockMovement,
)

from .serializers import (
    CategorySerializer,
    LocationSerializer,
    InventoryItemSerializer,
    StockMovementSerializer,
)

from .services import (
    add_stock,
    remove_stock,
    adjust_stock,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by("name")
    serializer_class = LocationSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all().order_by("name")
    serializer_class = InventoryItemSerializer

    @action(detail=True, methods=["post"], url_path="add-stock")
    def add_stock_action(self, request, pk=None):
        quantity = request.data.get("quantity")
        note = request.data.get("note", "")

        try:
            quantity = int(quantity)

            item = add_stock(
                item_id=pk,
                quantity=quantity,
                note=note,
            )

        except (TypeError, ValueError) as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            InventoryItemSerializer(item).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="remove-stock")
    def remove_stock_action(self, request, pk=None):
        quantity = request.data.get("quantity")
        note = request.data.get("note", "")

        try:
            quantity = int(quantity)

            item = remove_stock(
                item_id=pk,
                quantity=quantity,
                note=note,
            )

        except (TypeError, ValueError) as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            InventoryItemSerializer(item).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="adjust-stock")
    def adjust_stock_action(self, request, pk=None):
        quantity = request.data.get("quantity")
        note = request.data.get("note", "")

        try:
            quantity = int(quantity)

            item = adjust_stock(
                item_id=pk,
                new_quantity=quantity,
                note=note,
            )

        except (TypeError, ValueError) as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            InventoryItemSerializer(item).data,
            status=status.HTTP_200_OK,
        )


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.all().order_by("-created_at")
    serializer_class = StockMovementSerializer