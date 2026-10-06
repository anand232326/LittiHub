from typing import Any

from fastapi import APIRouter, Depends, Request

from app.clients.cart_client import cart_client
from app.core.security import (
    AuthenticatedUser,
    get_current_user,
)


router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"],
)


@router.get("")
async def get_cart(
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await cart_client.get_cart(
        token=request.headers["Authorization"],
    )


@router.post("/items")
async def add_item(
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await cart_client.add_item(
        data=data,
        token=request.headers["Authorization"],
    )


@router.patch("/items/{menu_item_id}")
async def update_item(
    menu_item_id: str,
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await cart_client.update_item(
        menu_item_id=menu_item_id,
        data=data,
        token=request.headers["Authorization"],
    )


@router.delete("/items/{menu_item_id}")
async def remove_item(
    menu_item_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await cart_client.remove_item(
        menu_item_id=menu_item_id,
        token=request.headers["Authorization"],
    )


@router.delete("")
async def clear_cart(
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await cart_client.clear_cart(
        token=request.headers["Authorization"],
    )


@router.get("/checkout")
async def checkout(
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await cart_client.checkout(
        token=request.headers["Authorization"],
    )