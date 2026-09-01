from app.models.restaurant import Restaurant
from app.repositories.restaurant_repository import restaurant_repository
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse,PaginatedResponse
from math import ceil
from app.utils.pagination import calculate_pagination
from app.core.enums import SortOrder, RestaurantSortField
from datetime import datetime, timezone
from app.schemas.restaurant import RestaurantResponse,RestaurantUpdate


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


    async def get_all(
    self,
    city: str | None = None,
    is_active: bool | None = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: RestaurantSortField = RestaurantSortField.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC,
    ) -> PaginatedResponse[RestaurantResponse]:

        restaurants, total = await self.restaurant_repository.get_all(
        city=city,
        is_active=is_active,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
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




    async def update(self,restaurant_id: str,restaurant_data: RestaurantUpdate,) -> RestaurantResponse | None:
        restaurant = await self.restaurant_repository.get_by_id(
            restaurant_id
        )

        if restaurant is None:
           return None

        update_data = restaurant_data.model_dump(
        exclude_unset=True
        )

        if not update_data:
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

        update_data["updated_at"] = datetime.now(timezone.utc)
        
        restaurant = await self.restaurant_repository.update(
        restaurant,
        update_data,
        )

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