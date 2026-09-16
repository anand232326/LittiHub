from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import (
    CreateRestaurantRequest,
    RestaurantResponse,
    UpdateRestaurantRequest,
)
from app.services.restaurant_service import RestaurantService


class RestaurantController:

    def __init__(self):
        restaurant_repository = RestaurantRepository()

        self.restaurant_service = RestaurantService(
            restaurant_repository=restaurant_repository
        )

    async def create_restaurant(
        self,
        request: CreateRestaurantRequest,
    ) -> RestaurantResponse:

        return await self.restaurant_service.create_restaurant(
            request
        )

    async def get_restaurant(
        self,
        restaurant_id: str,
    ) -> RestaurantResponse:

        return await self.restaurant_service.get_restaurant(
            restaurant_id
        )

    async def update_restaurant(
        self,
        restaurant_id: str,
        request: UpdateRestaurantRequest,
    ) -> RestaurantResponse:

        return await self.restaurant_service.update_restaurant(
            restaurant_id,
            request,
        )

    async def delete_restaurant(
        self,
        restaurant_id: str,
    ) -> RestaurantResponse:

        return await self.restaurant_service.delete_restaurant(
            restaurant_id
        )