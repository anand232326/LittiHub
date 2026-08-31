from app.models.restaurant import Restaurant
from app.repositories.restaurant_repository import restaurant_repository
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse,PaginatedResponse
from math import ceil
from app.utils.pagination import calculate_pagination

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


    async def get_by_id(self,restaurant_id:str,)->RestaurantResponse |None:
        restaurant=await self.restaurant_repository.get_by_id(restaurant_id)

        if restaurant is None:
            return None

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


    async def get_all(self,city:str |None=None,page:int=1,page_size:int=10)->PaginatedResponse[RestaurantResponse]:
        restaurants,total=await self.restaurant_repository.get_all(
            city=city,
            page=page,
            page_size=page_size,
        )
        pagination = calculate_pagination(
        page=page,
        page_size=page_size,
        total=total,
        )

        return PaginatedResponse(
        items=[
        RestaurantResponse(
            id=str(restaurant.id),
            name=restaurant.name,
            phone=restaurant.phone,
            address=restaurant.address,
            city=restaurant.city,
            is_active=restaurant.is_active,
            created_at=restaurant.created_at,
            updated_at=restaurant.updated_at,
        )
        for restaurant in restaurants
        ],
        **pagination,
        )


restaurant_service = RestaurantService()  