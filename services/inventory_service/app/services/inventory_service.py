from app.core.exceptions import (
    InvalidRequestError,
    ResourceNotFoundError,
)
from app.models.inventory import Inventory
from app.repositories.inventory_repository import (
    inventory_repository,
)


class InventoryService:

    async def create_inventory(
        self,
        restaurant_id: str,
        menu_item_id: str,
        quantity: int,
    ) -> Inventory:

        if quantity < 0:
            raise InvalidRequestError(
                "Quantity cannot be negative"
            )

        existing_inventory = (
            await inventory_repository.get_by_menu_item(
                restaurant_id=restaurant_id,
                menu_item_id=menu_item_id,
            )
        )

        if existing_inventory:

            raise InvalidRequestError(
                "Inventory already exists for this menu item"
            )

        inventory = Inventory(
            restaurant_id=restaurant_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
        )

        return await inventory_repository.create(
            inventory
        )

    async def get_inventory(
        self,
        inventory_id: str,
    ) -> Inventory:

        inventory = (
            await inventory_repository.get_by_id(
                inventory_id
            )
        )

        if not inventory:

            raise ResourceNotFoundError(
                "Inventory not found"
            )

        return inventory

    async def get_inventory_by_menu_item(
        self,
        restaurant_id: str,
        menu_item_id: str,
    ) -> Inventory:

        inventory = (
            await inventory_repository.get_by_menu_item(
                restaurant_id=restaurant_id,
                menu_item_id=menu_item_id,
            )
        )

        if not inventory:

            raise ResourceNotFoundError(
                "Inventory not found"
            )

        return inventory

    async def update_quantity(
        self,
        inventory_id: str,
        quantity: int,
    ) -> Inventory:

        if quantity < 0:

            raise InvalidRequestError(
                "Quantity cannot be negative"
            )

        inventory = (
            await inventory_repository.get_by_id(
                inventory_id
            )
        )

        if not inventory:

            raise ResourceNotFoundError(
                "Inventory not found"
            )

        inventory.quantity = quantity

        return await inventory_repository.update(
            inventory
        )

    async def reserve_stock(
        self,
        inventory_id: str,
        quantity: int,
    ) -> Inventory:

        if quantity <= 0:

            raise InvalidRequestError(
                "Reservation quantity must be greater than zero"
            )

        inventory = (
            await inventory_repository.get_by_id(
                inventory_id
            )
        )

        if not inventory:

            raise ResourceNotFoundError(
                "Inventory not found"
            )

        reserved_inventory = (
            await inventory_repository.reserve(
                inventory_id=inventory_id,
                quantity=quantity,
            )
        )

        if not reserved_inventory:

            raise InvalidRequestError(
                "Insufficient available inventory"
            )

        return reserved_inventory

    async def release_stock(
        self,
        inventory_id: str,
        quantity: int,
    ) -> Inventory:

        if quantity <= 0:

            raise InvalidRequestError(
                "Release quantity must be greater than zero"
            )

        inventory = (
            await inventory_repository.get_by_id(
                inventory_id
            )
        )

        if not inventory:

            raise ResourceNotFoundError(
                "Inventory not found"
            )

        released_inventory = (
            await inventory_repository.release(
                inventory_id=inventory_id,
                quantity=quantity,
            )
        )

        if not released_inventory:

            raise InvalidRequestError(
                "Cannot release more than the reserved quantity"
            )

        return released_inventory


inventory_service = InventoryService()