from app.schemas.inventory import (
    CreateInventoryRequest,
    InventoryResponse,
    UpdateInventoryRequest,
)
from app.services.inventory_service import (
    inventory_service,
)



class InventoryController:

    async def create_inventory(
        self,
        request: CreateInventoryRequest,
    ) -> InventoryResponse:

        inventory = await inventory_service.create_inventory(
            restaurant_id=request.restaurant_id,
            menu_item_id=request.menu_item_id,
            quantity=request.quantity,
        )

        return InventoryResponse(
            id=str(inventory.id),
            restaurant_id=inventory.restaurant_id,
            menu_item_id=inventory.menu_item_id,
            quantity=inventory.quantity,
            reserved_quantity=inventory.reserved_quantity,
            available_quantity=inventory.available_quantity,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )



    async def get_inventory(
        self,
        inventory_id: str,
    ) -> InventoryResponse:

        inventory = await inventory_service.get_inventory(
            inventory_id=inventory_id,
        )

        return InventoryResponse(
            id=str(inventory.id),
            restaurant_id=inventory.restaurant_id,
            menu_item_id=inventory.menu_item_id,
            quantity=inventory.quantity,
            reserved_quantity=inventory.reserved_quantity,
            available_quantity=inventory.available_quantity,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )




    async def get_inventory_by_menu_item(
        self,
        restaurant_id: str,
        menu_item_id: str,
    ) -> InventoryResponse:

        inventory = (
            await inventory_service
            .get_inventory_by_menu_item(
                restaurant_id=restaurant_id,
                menu_item_id=menu_item_id,
            )
        )

        return InventoryResponse(
            id=str(inventory.id),
            restaurant_id=inventory.restaurant_id,
            menu_item_id=inventory.menu_item_id,
            quantity=inventory.quantity,
            reserved_quantity=inventory.reserved_quantity,
            available_quantity=inventory.available_quantity,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )



    async def update_quantity(
        self,
        inventory_id: str,
        request: UpdateInventoryRequest,
    ) -> InventoryResponse:

        inventory = await inventory_service.update_quantity(
            inventory_id=inventory_id,
            quantity=request.quantity,
        )

        return InventoryResponse(
            id=str(inventory.id),
            restaurant_id=inventory.restaurant_id,
            menu_item_id=inventory.menu_item_id,
            quantity=inventory.quantity,
            reserved_quantity=inventory.reserved_quantity,
            available_quantity=inventory.available_quantity,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )




    async def reserve_stock(
        self,
        inventory_id: str,
        quantity: int,
    ) -> InventoryResponse:

        inventory = await inventory_service.reserve_stock(
            inventory_id=inventory_id,
            quantity=quantity,
        )

        return InventoryResponse(
            id=str(inventory.id),
            restaurant_id=inventory.restaurant_id,
            menu_item_id=inventory.menu_item_id,
            quantity=inventory.quantity,
            reserved_quantity=inventory.reserved_quantity,
            available_quantity=inventory.available_quantity,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )




    async def release_stock(
        self,
        inventory_id: str,
        quantity: int,
    ) -> InventoryResponse:

        inventory = await inventory_service.release_stock(
            inventory_id=inventory_id,
            quantity=quantity,
        )

        return InventoryResponse(
            id=str(inventory.id),
            restaurant_id=inventory.restaurant_id,
            menu_item_id=inventory.menu_item_id,
            quantity=inventory.quantity,
            reserved_quantity=inventory.reserved_quantity,
            available_quantity=inventory.available_quantity,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )


inventory_controller = InventoryController()