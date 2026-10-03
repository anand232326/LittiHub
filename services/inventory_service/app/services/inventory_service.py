from datetime import datetime, timezone
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

        existing_inventory = (
            await inventory_repository
            .get_by_restaurant_and_menu_item(
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
            reserved_quantity=0,
        )

        return await inventory_repository.create(
            inventory
        )



    async def get_inventory(
        self,
        inventory_id: str,
    ) -> Inventory:

        inventory = await inventory_repository.get_by_id(
            inventory_id
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
            await inventory_repository
            .get_by_restaurant_and_menu_item(
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

        inventory = await self.get_inventory(
            inventory_id
        )

        if quantity < inventory.reserved_quantity:
            raise InvalidRequestError(
                "Quantity cannot be less than reserved quantity"
            )

        inventory.quantity = quantity
        inventory.updated_at = datetime.now(
            timezone.utc
        )

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

        inventory = await self.get_inventory(
            inventory_id
        )

        if inventory.available_quantity < quantity:
            raise InvalidRequestError(
                "Insufficient inventory"
            )

        inventory.reserved_quantity += quantity

        inventory.updated_at = datetime.now(
            timezone.utc
        )

        return await inventory_repository.update(
            inventory
        )



    

    async def release_stock(
        self,
        inventory_id: str,
        quantity: int,
    ) -> Inventory:

        if quantity <= 0:
            raise InvalidRequestError(
                "Release quantity must be greater than zero"
            )

        inventory = await self.get_inventory(
            inventory_id
        )

        if inventory.reserved_quantity < quantity:
            raise InvalidRequestError(
                "Release quantity exceeds reserved quantity"
            )

        inventory.reserved_quantity -= quantity

        inventory.updated_at = datetime.now(
            timezone.utc
        )

        return await inventory_repository.update(
            inventory
        )




inventory_service = InventoryService()