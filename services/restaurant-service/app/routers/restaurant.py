from fastapi import APIRouter, Depends
from app.controllers.restaurant_controller import RestaurantController
from app.dependencies.auth import get_current_user,require_role
from app.schemas.restaurant import (
    CreateRestaurantRequest,
    RestaurantResponse,
    UpdateRestaurantRequest,
    RestaurantListResponse
)
from fastapi import APIRouter, Depends, Query
from app.core.enums import RestaurantSortField, SortOrder


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



@router.get(
    "",
    response_model=RestaurantListResponse,
)
async def list_restaurants(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    city: str | None = Query(
        default=None,
        min_length=2,
        max_length=100,
    ),
    is_active: bool | None = Query(
        default=True,
    ),
    is_open: bool | None = Query(
        default=None,
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    sort_by: RestaurantSortField = Query(
        default=RestaurantSortField.CREATED_AT,
    ),
    sort_order: SortOrder = Query(
        default=SortOrder.DESC,
    ),
    current_user: dict = Depends(get_current_user),
):
    return await restaurant_controller.list_restaurants(
        page=page,
        page_size=page_size,
        city=city,
        is_active=is_active,
        is_open=is_open,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )



@router.post("/{restaurant_id}/restore",response_model=RestaurantResponse,)
async def restore_restaurant(restaurant_id: str,current_user: dict = Depends(require_role("admin")),):
        return await restaurant_controller.restore_restaurant(
        restaurant_id
    )