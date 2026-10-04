from fastapi import APIRouter, status
from app.controllers.inventory_controller import (
    inventory_controller,
)
from app.schemas.inventory import (
    CreateInventoryRequest,
    InventoryResponse,
    UpdateInventoryRequest,
)




router = APIRouter(
    prefix="/api/v1/inventory",
    tags=["Inventory"],
)


@router.post(
    "",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory(
    request: CreateInventoryRequest,
) -> InventoryResponse:

    return await inventory_controller.create_inventory(
        request=request,
    )


@router.get(
    "/{inventory_id}",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_inventory(
    inventory_id: str,
) -> InventoryResponse:

    return await inventory_controller.get_inventory(
        inventory_id=inventory_id,
    )


@router.get(
    "/restaurant/{restaurant_id}/menu-item/{menu_item_id}",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_inventory_by_menu_item(
    restaurant_id: str,
    menu_item_id: str,
) -> InventoryResponse:

    return await (
        inventory_controller
        .get_inventory_by_menu_item(
            restaurant_id=restaurant_id,
            menu_item_id=menu_item_id,
        )
    )


@router.patch(
    "/{inventory_id}",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK,
)
async def update_inventory_quantity(
    inventory_id: str,
    request: UpdateInventoryRequest,
) -> InventoryResponse:

    return await inventory_controller.update_quantity(
        inventory_id=inventory_id,
        request=request,
    )


@router.post(
    "/{inventory_id}/reserve",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK,
)
async def reserve_inventory(
    inventory_id: str,
    quantity: int,
) -> InventoryResponse:

    return await inventory_controller.reserve_stock(
        inventory_id=inventory_id,
        quantity=quantity,
    )


@router.post(
    "/{inventory_id}/release",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK,
)
async def release_inventory(
    inventory_id: str,
    quantity: int,
) -> InventoryResponse:

    return await inventory_controller.release_stock(
        inventory_id=inventory_id,
        quantity=quantity,
    )