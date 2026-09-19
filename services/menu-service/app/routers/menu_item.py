from fastapi import APIRouter, Depends, status
from app.dependencies.auth import require_roles
from app.controllers.menu_item_controller import MenuItemController
from app.dependencies.menu import get_menu_item_controller
from app.schemas.menu_item import (
    CreateMenuItemRequest,
    UpdateMenuItemRequest,
    MenuItemResponse,
)

router = APIRouter(
    prefix="/restaurants/{restaurant_id}",
    tags=["Menu Items"],
)


@router.post(
    "/categories/{category_id}/items",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
    Depends(
        require_roles(
            "admin",
            "restaurant_admin",
        )
    )
]
)
async def create_item(
    restaurant_id: str,
    category_id: str,
    request: CreateMenuItemRequest,
    controller: MenuItemController = Depends(
        get_menu_item_controller
    ),
):
    # The category_id in the URL establishes the resource context.
    # We still keep category_id in the request schema for now,
    # but we should ensure both values match.
    if request.category_id != category_id:
        from app.core.exceptions import AppException

        raise AppException(
            "Category ID in URL and request body must match",
            status_code=400,
        )

    return await controller.create_item(
        restaurant_id=restaurant_id,
         category_id=category_id,
        request=request,
    )


@router.get(
    "/items/{item_id}",
    response_model=MenuItemResponse,
    dependencies=[
    Depends(
        require_roles(
            "admin",
            "restaurant_admin",
            "customer",
            "delivery_agent",
        )
    )
]
)
async def get_item(
    restaurant_id: str,
    item_id: str,
    controller: MenuItemController = Depends(
        get_menu_item_controller
    ),
):
    return await controller.get_item(
        restaurant_id=restaurant_id,
        item_id=item_id,
    )


@router.patch(
    "/items/{item_id}",
    response_model=MenuItemResponse,
    dependencies=[
    Depends(
        require_roles(
            "admin",
            "restaurant_admin",
        )
    )
]
)
async def update_item(
    restaurant_id: str,
    item_id: str,
    request: UpdateMenuItemRequest,
    controller: MenuItemController = Depends(
        get_menu_item_controller
    ),
):
    return await controller.update_item(
        restaurant_id=restaurant_id,
        item_id=item_id,
        request=request,
    )


@router.delete(
    "/items/{item_id}",
    response_model=MenuItemResponse,
    dependencies=[
    Depends(
        require_roles(
            "admin",
        )
    )
]
)
async def delete_item(
    restaurant_id: str,
    item_id: str,
    controller: MenuItemController = Depends(
        get_menu_item_controller
    ),
):
    return await controller.delete_item(
        restaurant_id=restaurant_id,
        item_id=item_id,
    )


@router.post(
    "/items/{item_id}/restore",
    response_model=MenuItemResponse,
    dependencies=[
    Depends(
        require_roles(
            "admin",
        )
    )
]
)
async def restore_item(
    restaurant_id: str,
    item_id: str,
    controller: MenuItemController = Depends(
        get_menu_item_controller
    ),
):
    return await controller.restore_item(
        restaurant_id=restaurant_id,
        item_id=item_id,
    )