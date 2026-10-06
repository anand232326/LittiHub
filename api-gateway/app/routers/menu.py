from typing import Any

from fastapi import APIRouter, Depends, Request

from app.clients.menu_client import menu_client
from app.core.security import (
    AuthenticatedUser,
    get_current_user,
)


router = APIRouter(
    prefix="/api/v1/restaurants",
    tags=["Menu"],
)


@router.post("/{restaurant_id}/categories")
async def create_category(
    restaurant_id: str,
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await menu_client.create_category(
        restaurant_id=restaurant_id,
        data=data,
        token=request.headers["Authorization"],
    )


@router.post(
    "/{restaurant_id}/categories/{category_id}/items"
)
async def create_menu_item(
    restaurant_id: str,
    category_id: str,
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await menu_client.create_menu_item(
        restaurant_id=restaurant_id,
        category_id=category_id,
        data=data,
        token=request.headers["Authorization"],
    )


@router.get(
    "/{restaurant_id}/items/{item_id}"
)
async def get_menu_item(
    restaurant_id: str,
    item_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await menu_client.get_menu_item(
        restaurant_id=restaurant_id,
        item_id=item_id,
        token=request.headers["Authorization"],
    )


@router.patch(
    "/{restaurant_id}/items/{item_id}"
)
async def update_menu_item(
    restaurant_id: str,
    item_id: str,
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await menu_client.update_menu_item(
        restaurant_id=restaurant_id,
        item_id=item_id,
        data=data,
        token=request.headers["Authorization"],
    )


@router.delete(
    "/{restaurant_id}/items/{item_id}"
)
async def delete_menu_item(
    restaurant_id: str,
    item_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await menu_client.delete_menu_item(
        restaurant_id=restaurant_id,
        item_id=item_id,
        token=request.headers["Authorization"],
    )


@router.post(
    "/{restaurant_id}/items/{item_id}/restore"
)
async def restore_menu_item(
    restaurant_id: str,
    item_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await menu_client.restore_menu_item(
        restaurant_id=restaurant_id,
        item_id=item_id,
        token=request.headers["Authorization"],
    )