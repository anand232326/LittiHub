from datetime import datetime, timezone
from beanie import SortDirection
from bson import ObjectId
from bson.errors import InvalidId
from app.core.enums import RestaurantSortField, SortOrder
from app.models.restaurant import Restaurant



class RestaurantRepository:


    async def create(
    self,
    restaurant: Restaurant,
    ) -> Restaurant:

        await restaurant.insert()

        return restaurant


    async def get_by_id(
    self,
    restaurant_id: str,
    ) -> Restaurant | None:

        try:
            object_id = ObjectId(restaurant_id)

        except InvalidId:
            return None

        return await Restaurant.find_one(
        {
            "_id": object_id,
            "is_deleted": False,
        }
        )


    async def get_all(
    self,
    city: str | None = None,
    is_active: bool | None = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: RestaurantSortField = RestaurantSortField.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC,
    ) -> tuple[list[Restaurant], int]:

        query = {
        "is_deleted": False,
        }

        if city:
            query["city"] = city

        if is_active is not None:
            query["is_active"] = is_active

        total = await Restaurant.find(query).count()

        skip = (page - 1) * page_size

        sort_direction = (
        SortDirection.ASCENDING
        if sort_order == SortOrder.ASC
        else SortDirection.DESCENDING
        )

        restaurants = await (
        Restaurant.find(query)
        .sort(
            (sort_by.value, sort_direction)
        )
        .skip(skip)
        .limit(page_size)
        .to_list()
        )

        return restaurants, total


    async def update(
    self,
    restaurant: Restaurant,
    update_data: dict,
    ) -> Restaurant:

        await restaurant.set(update_data)

        return restaurant


    async def soft_delete(
        self,
    restaurant: Restaurant,
    ) -> Restaurant:

        await restaurant.set(
        {
            "is_deleted": True,
            "is_active": False,
            "updated_at": datetime.now(timezone.utc),
        }
        )

        return restaurant


    async def get_deleted_by_id(
    self,
    restaurant_id: str,
    ) -> Restaurant | None:

        try:
            object_id = ObjectId(restaurant_id)

        except InvalidId:
            return None

        return await Restaurant.find_one(
        {
            "_id": object_id,
            "is_deleted": True,
        }
        )


    async def restore(
    self,
    restaurant: Restaurant,
    ) -> Restaurant:

        await restaurant.set(
        {
            "is_deleted": False,
            "is_active": True,
            "updated_at": datetime.now(timezone.utc),
        }
        )

        return restaurant


restaurant_repository = RestaurantRepository()
