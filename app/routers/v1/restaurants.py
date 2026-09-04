from fastapi import APIRouter, Depends, Query, status
from app.controllers.restaurant_controller import restaurant_controller
from app.core.enums import RestaurantSortField, SortOrder, UserRole
from app.dependencies.auth import get_current_user, require_role
from app.models.user import User
from app.schemas.restaurant import (
PaginatedResponse,
RestaurantCreate,
RestaurantResponse,
RestaurantUpdate,
)

router = APIRouter(
prefix="/restaurants",
tags=["Restaurants"],
)


@router.post("/",response_model=RestaurantResponse,)
async def create_restaurant(restaurant_data: RestaurantCreate,current_user: User = Depends(require_role(UserRole.ADMIN)),):
    return await restaurant_controller.create(
        restaurant_data=restaurant_data,
        current_user=current_user,
    )


@router.get("/",response_model=PaginatedResponse[RestaurantResponse],)
async def get_restaurants(city: str | None = None,is_active: bool | None = None,
    page: int = Query(default=1,ge=1,),page_size: int = Query(default=10,ge=1,le=100,),
    sort_by: RestaurantSortField = RestaurantSortField.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC,):

    return await restaurant_controller.get_all(
        city=city,
        is_active=is_active,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/{restaurant_id}",response_model=RestaurantResponse,)
async def get_restaurant(restaurant_id: str,):
    return await restaurant_controller.get_by_id(
        restaurant_id=restaurant_id,
    )


@router.patch("/{restaurant_id}",response_model=RestaurantResponse,)
async def update_restaurant(restaurant_id: str,restaurant_data: RestaurantUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),):

    return await restaurant_controller.update(
        restaurant_id=restaurant_id,
        restaurant_data=restaurant_data,
        current_user=current_user,
    )


@router.delete("/{restaurant_id}",status_code=status.HTTP_204_NO_CONTENT,)
async def delete_restaurant(restaurant_id: str,current_user: User = Depends(require_role(UserRole.ADMIN)),):

    await restaurant_controller.delete(
        restaurant_id=restaurant_id,
        current_user=current_user,
    )


@router.patch("/{restaurant_id}/restore",response_model=RestaurantResponse,)
async def restore_restaurant(restaurant_id: str,_: User = Depends(require_role(UserRole.ADMIN)),):

    return await restaurant_controller.restore(
        restaurant_id=restaurant_id,
    )

