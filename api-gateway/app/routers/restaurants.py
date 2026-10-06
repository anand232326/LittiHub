from typing import Any

from fastapi import APIRouter, Depends, Request

from app.clients.restaurant_client import restaurant_client
from app.core.security import (
    AuthenticatedUser,
    get_current_user,
)


router = APIRouter(
    prefix="/api/v1/restaurants",
    tags=["Restaurants"],
)


@router.post("/")
async def create_restaurant(
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await restaurant_client.create_restaurant(
        data=data,
        token=request.headers["Authorization"],
    )


@router.get("")
async def get_restaurants(
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await restaurant_client.get_restaurants(
        token=request.headers["Authorization"],
    )


@router.get("/{restaurant_id}")
async def get_restaurant(
    restaurant_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await restaurant_client.get_restaurant(
        restaurant_id=restaurant_id,
        token=request.headers["Authorization"],
    )


@router.patch("/{restaurant_id}")
async def update_restaurant(
    restaurant_id: str,
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await restaurant_client.update_restaurant(
        restaurant_id=restaurant_id,
        data=data,
        token=request.headers["Authorization"],
    )


@router.delete("/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await restaurant_client.delete_restaurant(
        restaurant_id=restaurant_id,
        token=request.headers["Authorization"],
    )


@router.post("/{restaurant_id}/restore")
async def restore_restaurant(
    restaurant_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await restaurant_client.restore_restaurant(
        restaurant_id=restaurant_id,
        token=request.headers["Authorization"],
    )
