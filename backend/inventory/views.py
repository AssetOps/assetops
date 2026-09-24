from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Location, Product, StockLevel, StockMovement
from .serializers import (
    CategorySerializer,
    LocationSerializer,
    ProductSerializer,
    StockAdjustmentSerializer,
    StockChangeSerializer,
    StockLevelSerializer,
    StockMovementSerializer,
)
from .services import add_stock, adjust_stock, remove_stock


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by("name")
    serializer_class = LocationSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all().order_by("name")
    serializer_class = ProductSerializer

    @action(detail=True, methods=["post"], url_path="add-stock")
    def add_stock_action(self, request, pk=None):
        product = self.get_object()

        serializer = StockChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            stock_level, movement = add_stock(
                product=product,
                location=serializer.validated_data["location"],
                quantity=serializer.validated_data["quantity"],
                reason=serializer.validated_data.get("reason", ""),
            )
        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "stock_level": StockLevelSerializer(stock_level).data,
                "movement": StockMovementSerializer(movement).data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="remove-stock")
    def remove_stock_action(self, request, pk=None):
        product = self.get_object()

        serializer = StockChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            stock_level, movement = remove_stock(
                product=product,
                location=serializer.validated_data["location"],
                quantity=serializer.validated_data["quantity"],
                reason=serializer.validated_data.get("reason", ""),
            )
        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "stock_level": StockLevelSerializer(stock_level).data,
                "movement": StockMovementSerializer(movement).data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="adjust-stock")
    def adjust_stock_action(self, request, pk=None):
        product = self.get_object()

        serializer = StockAdjustmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            stock_level, movement = adjust_stock(
                product=product,
                location=serializer.validated_data["location"],
                new_quantity=serializer.validated_data["quantity"],
                reason=serializer.validated_data.get("reason", ""),
            )
        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = {
            "stock_level": StockLevelSerializer(stock_level).data,
            "movement": (StockMovementSerializer(movement).data if movement else None),
        }

        return Response(
            response,
            status=status.HTTP_200_OK,
        )


class StockLevelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StockLevelSerializer

    def get_queryset(self):
        queryset = StockLevel.objects.select_related(
            "product",
            "location",
        ).all()

        product = self.request.query_params.get("product")
        location = self.request.query_params.get("location")

        if product:
            queryset = queryset.filter(product_id=product)

        if location:
            queryset = queryset.filter(location_id=location)

        return queryset.order_by("product__name")


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.select_related(
        "product",
        "location",
    ).order_by("-created_at")

    serializer_class = StockMovementSerializer
