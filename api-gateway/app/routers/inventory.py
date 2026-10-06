from typing import Any

from fastapi import APIRouter, Depends, Request

from app.clients.inventory_client import inventory_client
from app.core.security import (
    AuthenticatedUser,
    get_current_user,
)


router = APIRouter(
    prefix="/api/v1/inventory",
    tags=["Inventory"],
)


@router.post("")
async def create_inventory(
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await inventory_client.create_inventory(
        data=data,
        token=request.headers["Authorization"],
    )


@router.get("/{inventory_id}")
async def get_inventory(
    inventory_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await inventory_client.get_inventory(
        inventory_id=inventory_id,
        token=request.headers["Authorization"],
    )


@router.get(
    "/restaurant/{restaurant_id}/menu-item/{menu_item_id}"
)
async def get_inventory_by_menu_item(
    restaurant_id: str,
    menu_item_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await inventory_client.get_inventory_by_menu_item(
        restaurant_id=restaurant_id,
        menu_item_id=menu_item_id,
        token=request.headers["Authorization"],
    )


@router.patch("/{inventory_id}")
async def update_inventory(
    inventory_id: str,
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await inventory_client.update_inventory(
        inventory_id=inventory_id,
        data=data,
        token=request.headers["Authorization"],
    )


@router.post("/{inventory_id}/reserve")
async def reserve_inventory(
    inventory_id: str,
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await inventory_client.reserve_inventory(
        inventory_id=inventory_id,
        data=data,
        token=request.headers["Authorization"],
    )


@router.post("/{inventory_id}/release")
async def release_inventory(
    inventory_id: str,
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await inventory_client.release_inventory(
        inventory_id=inventory_id,
        data=data,
        token=request.headers["Authorization"],
    )