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
        return await Restaurant.get(ObjectId(restaurant_id))

    async def get_by_slug(
        self,
        slug: str,
    ) -> Optional[Restaurant]:
        return await Restaurant.find_one(Restaurant.slug == slug)

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