from fastapi import APIRouter, Depends
from app.controllers.restaurant_controller import RestaurantController
from app.dependencies.auth import get_current_user,require_role
from app.schemas.restaurant import (
    CreateRestaurantRequest,
    RestaurantResponse,
    UpdateRestaurantRequest,
)


router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)

restaurant_controller = RestaurantController()


@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=201,
)
async def create_restaurant(
    request: CreateRestaurantRequest,
    current_user: dict = Depends(
        require_role("admin", "restaurant_admin")
    ),
):
    return await restaurant_controller.create_restaurant(
        request
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
async def get_restaurant(
    restaurant_id: str,
    current_user: dict = Depends(get_current_user),
):
    return await restaurant_controller.get_restaurant(
        restaurant_id
    )


@router.patch(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
async def update_restaurant(
    restaurant_id: str,
    request: UpdateRestaurantRequest,
    current_user: dict = Depends(
        require_role("admin", "restaurant_admin")
    ),
):
    return await restaurant_controller.update_restaurant(
        restaurant_id,
        request,
    )


@router.delete(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
async def delete_restaurant(
    restaurant_id: str,
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    return await restaurant_controller.delete_restaurant(
        restaurant_id
    )