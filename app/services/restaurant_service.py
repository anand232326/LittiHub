from app.models.restaurant import Restaurant
from app.repositories.restaurant_repository import restaurant_repository
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse


class RestaurantService:
    def __init__(self):
        self.restaurant_repository = restaurant_repository

    async def create(self,restaurant_data:RestaurantCreate,)->RestaurantResponse:
        restaurant=Restaurant(
            name=restaurant_data.name,
            phone=restaurant_data.phone,
            address=restaurant_data.address,
            city=restaurant_data.city,
        )
        restaurant=await self.restaurant_repository.create(restaurant)

        return RestaurantResponse(
            id=str(restaurant.id),
            name=restaurant.name,
            phone=restaurant.phone,
            address=restaurant.address,
            city=restaurant.city,
            is_active=restaurant.is_active,
            created_at=restaurant.created_at,
            updated_at=restaurant.updated_at,
        )   

restaurant_service = RestaurantService()  