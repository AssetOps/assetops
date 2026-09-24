from decimal import Decimal

from django.db import transaction

from .models import Product, StockLevel, StockMovement


def _get_stock_level(product: Product, location):
    stock_level, _ = StockLevel.objects.get_or_create(
        product=product,
        location=location,
        defaults={
            "quantity_on_hand": Decimal(0),
        },
    )

    return StockLevel.objects.select_for_update().get(
        pk=stock_level.pk,
    )


@transaction.atomic
def add_stock(product, location, quantity, reason=""):
    quantity = Decimal(quantity)

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    stock_level = _get_stock_level(product, location)

    stock_level.quantity_on_hand += quantity
    stock_level.save()

    movement = StockMovement.objects.create(
        product=product,
        location=location,
        quantity=quantity,
        reason=reason or "add",
    )

    return stock_level, movement


@transaction.atomic
def remove_stock(product, location, quantity, reason=""):
    quantity = Decimal(quantity)

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    stock_level = _get_stock_level(product, location)

    if stock_level.quantity_on_hand < quantity:
        raise ValueError("Not enough stock at this location.")

    stock_level.quantity_on_hand -= quantity
    stock_level.save()

    movement = StockMovement.objects.create(
        product=product,
        location=location,
        quantity=-quantity,
        reason=reason or "remove",
    )

    return stock_level, movement


@transaction.atomic
def adjust_stock(product, location, new_quantity, reason=""):
    new_quantity = Decimal(new_quantity)

    if new_quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    stock_level = _get_stock_level(product, location)

    difference = new_quantity - stock_level.quantity_on_hand

    stock_level.quantity_on_hand = new_quantity
    stock_level.save()

    movement = None

    if difference != 0:
        movement = StockMovement.objects.create(
            product=product,
            location=location,
            quantity=difference,
            reason=reason or "adjust",
        )

    return stock_level, movement
