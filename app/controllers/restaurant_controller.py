from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
)
from app.services.restaurant_service import restaurant_service


class RestaurantController:

    async def create(self,restaurant_data: RestaurantCreate,) -> RestaurantResponse:
        return await restaurant_service.create(
            restaurant_data
        )


restaurant_controller = RestaurantController()