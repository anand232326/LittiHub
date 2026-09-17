from typing import Optional
from bson import ObjectId
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
    ) -> Optional[Restaurant]:

        if not ObjectId.is_valid(restaurant_id):
            return None

        return await Restaurant.get(
            ObjectId(restaurant_id)
        )

    async def get_by_slug(
        self,
        slug: str,
    ) -> Optional[Restaurant]:

        return await Restaurant.find_one(
            Restaurant.slug == slug
        )

    async def update(
        self,
        restaurant: Restaurant,
    ) -> Restaurant:

        await restaurant.save()

        return restaurant

    async def delete(
        self,
        restaurant: Restaurant,
    ) -> Restaurant:

        restaurant.is_active = False

        await restaurant.save()

        return restaurant

    async def list_restaurants(
        self,
        skip: int,
        limit: int,
        city: str | None = None,
        is_active: bool | None = True,
        is_open: bool | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_order: int = -1,
    ) -> tuple[list[Restaurant], int]:

        filters = {}

        # Filter by city
        if city:
            filters["city"] = {
                "$regex": f"^{city}$",
                "$options": "i",
            }

        # Filter by active status
        if is_active is not None:
            filters["is_active"] = is_active

        # Filter by open status
        if is_open is not None:
            filters["is_open"] = is_open

        # Search restaurant name
        if search:
            filters["name"] = {
                "$regex": search,
                "$options": "i",
            }

        query = Restaurant.find(filters)

        total = await query.count()

        restaurants = await (
            query
            .sort((sort_by, sort_order))
            .skip(skip)
            .limit(limit)
            .to_list()
        )

        return restaurants, total