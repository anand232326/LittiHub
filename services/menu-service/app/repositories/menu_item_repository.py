from typing import Optional
from bson import ObjectId
from app.models.menu_item import MenuItem


class MenuItemRepository:

    async def create(
        self,
        item: MenuItem,
    ) -> MenuItem:

        await item.insert()

        return item

    async def get_by_id(
        self,
        item_id: str,
    ) -> Optional[MenuItem]:

        if not ObjectId.is_valid(item_id):
            return None

        return await MenuItem.get(
            ObjectId(item_id)
        )

    async def get_by_restaurant_and_id(
        self,
        restaurant_id: str,
        item_id: str,
    ) -> Optional[MenuItem]:

        return await MenuItem.find_one(
            MenuItem.id == item_id,
            MenuItem.restaurant_id == restaurant_id,
        )

    async def get_by_category_and_name(
        self,
        category_id: str,
        name: str,
    ) -> Optional[MenuItem]:

        return await MenuItem.find_one(
            MenuItem.category_id == category_id,
            MenuItem.name == name,
        )

    async def update(
        self,
        item: MenuItem,
    ) -> MenuItem:

        await item.save()

        return item

    async def delete(
        self,
        item: MenuItem,
    ) -> MenuItem:

        item.is_active = False

        await item.save()

        return item



    async def restore(
    self,
    item: MenuItem,
    ) -> MenuItem:

        item.is_active = True
        await item.save()
        return item