from app.models.inventory import Inventory
from app.schemas.inventory import (
    CreateInventoryRequest,
    UpdateInventoryRequest,
)
from app.services.inventory_service import (
    inventory_service,
)


class InventoryController:

    async def create_inventory(
        self,
        request: CreateInventoryRequest,
    ) -> Inventory:

        return await inventory_service.create_inventory(
            restaurant_id=request.restaurant_id,
            menu_item_id=request.menu_item_id,
            quantity=request.quantity,
        )

    async def get_inventory(
        self,
        inventory_id: str,
    ) -> Inventory:

        return await inventory_service.get_inventory(
            inventory_id=inventory_id,
        )

    async def get_inventory_by_menu_item(
        self,
        restaurant_id: str,
        menu_item_id: str,
    ) -> Inventory:

        return await (
            inventory_service
            .get_inventory_by_menu_item(
                restaurant_id=restaurant_id,
                menu_item_id=menu_item_id,
            )
        )

    async def update_quantity(
        self,
        inventory_id: str,
        request: UpdateInventoryRequest,
    ) -> Inventory:

        return await inventory_service.update_quantity(
            inventory_id=inventory_id,
            quantity=request.quantity,
        )

    async def reserve_stock(
        self,
        inventory_id: str,
        quantity: int,
    ) -> Inventory:

        return await inventory_service.reserve_stock(
            inventory_id=inventory_id,
            quantity=quantity,
        )

    async def release_stock(
        self,
        inventory_id: str,
        quantity: int,
    ) -> Inventory:

        return await inventory_service.release_stock(
            inventory_id=inventory_id,
            quantity=quantity,
        )


inventory_controller = InventoryController()