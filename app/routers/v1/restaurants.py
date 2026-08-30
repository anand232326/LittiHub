from fastapi import APIRouter, Depends
from app.controllers.restaurant_controller import restaurant_controller
from app.dependencies.auth import require_role
from app.core.enums import UserRole
from app.models.user import User
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
)


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