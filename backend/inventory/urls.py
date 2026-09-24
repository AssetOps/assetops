from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    LocationViewSet,
    InventoryItemViewSet,
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
    "items",
    InventoryItemViewSet,
    basename="item",
)

router.register(
    "stock-movements",
    StockMovementViewSet,
    basename="stock-movement",
)


urlpatterns = [
    path("", include(router.urls)),
]