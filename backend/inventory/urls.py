from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    LocationViewSet,
    ProductViewSet,
    StockLevelViewSet,
    StockMovementViewSet,
)

router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet,
    basename="category",
)

router.register(
    "locations",
    LocationViewSet,
    basename="location",
)

router.register(
    "products",
    ProductViewSet,
    basename="product",
)

router.register(
    "stock-levels",
    StockLevelViewSet,
    basename="stock-level",
)

router.register(
    "stock-movements",
    StockMovementViewSet,
    basename="stock-movement",
)


urlpatterns = [
    path("", include(router.urls)),
]
