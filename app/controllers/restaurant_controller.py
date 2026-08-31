from fastapi import HTTPException, status
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
    PaginatedResponse
)
from app.services.restaurant_service import restaurant_service


class RestaurantController:

    async def create(self,restaurant_data: RestaurantCreate,) -> RestaurantResponse:
        return await restaurant_service.create(
            restaurant_data
        )


    async def get_by_id(self,restaurant_id:str,)->RestaurantResponse:
        restaurant=await restaurant_service.get_by_id(restaurant_id)

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="restaurant not found"
            )
        return restaurant


    async def get_all(self,city: str | None = None,page: int = 1,page_size: int = 10,) -> PaginatedResponse[RestaurantResponse]:
        return await restaurant_service.get_all(
            city=city,
            page=page,
            page_size=page_size,
        ) 



restaurant_controller = RestaurantController()