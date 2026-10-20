from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from app.clients.cart_client import cart_client
from app.core.security import (
    AuthenticatedUser,
    get_current_user,
)


router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"],
)


def _get_auth_header(request: Request) -> str:
    """Safely extract the Authorization header from the incoming request."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return auth_header


@router.get("")
async def get_cart(
    request: Request,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return await cart_client.get_cart(
        token=_get_auth_header(request),
    )


@router.post("/items")
async def add_item(
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return await cart_client.add_item(
        data=data,
        token=_get_auth_header(request),
    )


@router.patch("/items/{menu_item_id}")
async def update_item(
    menu_item_id: str,
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return await cart_client.update_item(
        menu_item_id=menu_item_id,
        data=data,
        token=_get_auth_header(request),
    )


@router.delete("/items/{menu_item_id}")
async def remove_item(
    menu_item_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return await cart_client.remove_item(
        menu_item_id=menu_item_id,
        token=_get_auth_header(request),
    )


@router.delete("")
async def clear_cart(
    request: Request,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return await cart_client.clear_cart(
        token=_get_auth_header(request),
    )


@router.get("/checkout")
async def checkout(
    request: Request,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return await cart_client.checkout(
        token=_get_auth_header(request),
    )