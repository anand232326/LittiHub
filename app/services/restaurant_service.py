from datetime import datetime, timezone

from app.core.enums import RestaurantSortField, SortOrder
from app.models.restaurant import Restaurant
from app.repositories.restaurant_repository import restaurant_repository
from app.schemas.restaurant import (
PaginatedResponse,
RestaurantCreate,
RestaurantResponse,
RestaurantUpdate,
)
from app.utils.pagination import calculate_pagination

class RestaurantService:

    def __init__(self):
        self.restaurant_repository = restaurant_repository


    async def create(
    self,
    restaurant_data: RestaurantCreate,
    owner_id: str,
    ) -> RestaurantResponse:

        restaurant = Restaurant(
            outlet_name=restaurant_data.outlet_name,
            phone=restaurant_data.phone,
            address=restaurant_data.address,
            city=restaurant_data.city,
            locality=restaurant_data.locality,
            pincode=restaurant_data.pincode,
            latitude=restaurant_data.latitude,
            longitude=restaurant_data.longitude,
            owner_id=owner_id,
        )

        restaurant = await self.restaurant_repository.create(
        restaurant
        )

        return self._to_response(restaurant)


    async def get_by_id(
    self,
    restaurant_id: str,
    ) -> RestaurantResponse | None:

        restaurant = await self.restaurant_repository.get_by_id(
        restaurant_id
        )

        if restaurant is None:
            return None

        return self._to_response(restaurant)


    async def get_all(
    self,
    city: str | None = None,
    is_active: bool | None = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: RestaurantSortField = RestaurantSortField.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC,
    ) -> PaginatedResponse[RestaurantResponse]:

        restaurants, total = (
            await self.restaurant_repository.get_all(
                city=city,
                is_active=is_active,
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_order=sort_order,
            )
        )

        pagination = calculate_pagination(
        page=page,
        page_size=page_size,
        total=total,
        )

        return PaginatedResponse(
        items=[
            self._to_response(restaurant)
            for restaurant in restaurants
        ],
        **pagination,
        )


    async def update(
    self,
    restaurant_id: str,
    restaurant_data: RestaurantUpdate,
    ) -> RestaurantResponse | None:

        restaurant = await self.restaurant_repository.get_by_id(
        restaurant_id
        )

        if restaurant is None:
            return None

        update_data = restaurant_data.model_dump(
        exclude_unset=True
        )

        if not update_data:
            return self._to_response(restaurant)

        update_data["updated_at"] = datetime.now(
        timezone.utc
        )

        restaurant = await self.restaurant_repository.update(
        restaurant,
        update_data,
        )

        return self._to_response(restaurant)


    async def delete(
    self,
    restaurant_id: str,
    ) -> bool:

        restaurant = await self.restaurant_repository.get_by_id(
        restaurant_id
        )

        if restaurant is None:
            return False

        await self.restaurant_repository.soft_delete(
        restaurant
        )

        return True


    async def restore(
    self,
    restaurant_id: str,
    ) -> RestaurantResponse | None:

        restaurant = (
        await self.restaurant_repository.get_deleted_by_id(
            restaurant_id
        )
        )

        if restaurant is None:
            return None

        restaurant = await self.restaurant_repository.restore(
        restaurant
        )

        return self._to_response(restaurant)


    def _to_response(
    self,
    restaurant: Restaurant,
    ) -> RestaurantResponse:

        return RestaurantResponse(
        id=str(restaurant.id),
        outlet_name=restaurant.outlet_name,
        phone=restaurant.phone,
        address=restaurant.address,
        city=restaurant.city,
        locality=restaurant.locality,
        pincode=restaurant.pincode,
        latitude=restaurant.latitude,
        longitude=restaurant.longitude,
        is_active=restaurant.is_active,
        created_at=restaurant.created_at,
        updated_at=restaurant.updated_at,
        )


restaurant_service = RestaurantService()
