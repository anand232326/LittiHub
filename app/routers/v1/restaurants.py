from fastapi import APIRouter, Depends, HTTPException, status
from app.controllers.restaurant_controller import restaurant_controller
from app.dependencies.auth import require_role
from app.core.enums import UserRole
from app.models.user import User
from app.schemas.restaurant import RestaurantCreate,RestaurantResponse,PaginatedResponse,RestaurantUpdate
from fastapi import Query
from app.core.enums import SortOrder, RestaurantSortField

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)


@router.post( "/", response_model=RestaurantResponse, status_code=201,)
async def create_restaurant(restaurant_data: RestaurantCreate,
current_user: User = Depends(require_role(UserRole.ADMIN)),):
    return await restaurant_controller.create(
        restaurant_data
    )


@router.get("/{restaurant_id}",response_model=RestaurantResponse)
async def get_restaurant(restaurant_id:str):
    restaurant = await restaurant_controller.get_by_id(restaurant_id)
    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with id '{restaurant_id}' not found",
        )
        
    return restaurant


@router.get(
    "/",
    response_model=PaginatedResponse[RestaurantResponse],
)
async def get_restaurants(

    city: str | None = None,

    is_active: bool | None = None,

    page: int = Query(
        default=1,
        ge=1,
    ),

    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),

    sort_by: RestaurantSortField = RestaurantSortField.CREATED_AT,

    sort_order: SortOrder = SortOrder.DESC,
):

    return await restaurant_controller.get_all(
        city=city,
        is_active=is_active,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.patch("/{restaurant_id}",response_model=RestaurantResponse,)
async def update_restaurant(restaurant_id: str,restaurant_data: RestaurantUpdate,):
    return await restaurant_controller.update(
        restaurant_id,
        restaurant_data,
    )