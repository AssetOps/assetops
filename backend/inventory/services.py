from django.db import transaction

from .models import InventoryItem, StockMovement


@transaction.atomic
def add_stock(item_id, quantity, note=""):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    item = InventoryItem.objects.select_for_update().get(id=item_id)

    item.quantity += quantity
    item.save(update_fields=["quantity"])

    StockMovement.objects.create(
        item=item,
        movement_type=StockMovement.MovementType.ADD,
        quantity=quantity,
        note=note,
    )

    return item


@transaction.atomic
def remove_stock(item_id, quantity, note=""):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    item = InventoryItem.objects.select_for_update().get(id=item_id)

    if quantity > item.quantity:
        raise ValueError("Not enough stock.")

    item.quantity -= quantity
    item.save(update_fields=["quantity"])

    StockMovement.objects.create(
        item=item,
        movement_type=StockMovement.MovementType.REMOVE,
        quantity=quantity,
        note=note,
    )

    return item


@transaction.atomic
def adjust_stock(item_id, new_quantity, note=""):
    if new_quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    item = InventoryItem.objects.select_for_update().get(id=item_id)

    difference = abs(new_quantity - item.quantity)

    item.quantity = new_quantity
    item.save(update_fields=["quantity"])

    StockMovement.objects.create(
        item=item,
        movement_type=StockMovement.MovementType.ADJUST,
        quantity=difference,
        note=note,
    )

    return item