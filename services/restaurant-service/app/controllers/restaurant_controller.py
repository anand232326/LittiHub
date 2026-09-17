from app.repositories.restaurant_repository import RestaurantRepository
from app.core.enums import RestaurantSortField, SortOrder

from app.schemas.restaurant import (
    CreateRestaurantRequest,
    RestaurantListResponse,
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



    async def list_restaurants(
    self,
    page: int,
    page_size: int,
    city: str | None = None,
    is_active: bool | None = True,
    is_open: bool | None = None,
    search: str | None = None,
    sort_by: RestaurantSortField = RestaurantSortField.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC,
    ) -> RestaurantListResponse:

        return await self.restaurant_service.list_restaurants(
        page=page,
        page_size=page_size,
        city=city,
        is_active=is_active,
        is_open=is_open,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )



    async def restore_restaurant(
    self,
    restaurant_id: str,
    ) -> RestaurantResponse:

        return await self.restaurant_service.restore_restaurant(
        restaurant_id
    )