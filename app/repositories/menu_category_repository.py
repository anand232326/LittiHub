from datetime import datetime, timezone
from beanie import SortDirection
from bson import ObjectId
from bson.errors import InvalidId
from app.models.menu_category import MenuCategory
from app.core.enums import SortOrder

class MenuCategoryRepository:


    async def create(
    self,
    category: MenuCategory,
    ) -> MenuCategory:

        await category.insert()
        return category


    async def get_by_id(
    self,
    category_id: str,
    ) -> MenuCategory | None:

        try:
            object_id = ObjectId(category_id)
        except InvalidId:
            return None

        return await MenuCategory.find_one(
        {
            "_id": object_id,
            "is_deleted": False,
        }
        )


    async def get_all_by_restaurant(
    self,
    restaurant_id: str,
    is_active: bool | None = None,
    sort_order: SortOrder = SortOrder.ASC,
    ) -> list[MenuCategory]:

        query = {
        "restaurant_id": restaurant_id,
        "is_deleted": False,
        }

        if is_active is not None:
            query["is_active"] = is_active

        sort_direction = (
        SortDirection.ASCENDING
        if sort_order == SortOrder.ASC
        else SortDirection.DESCENDING
        )

        return await (
        MenuCategory.find(query)
        .sort("name", sort_direction)
        .to_list()
        )


    async def update(
    self,
    category: MenuCategory,
    update_data: dict,
    ) -> MenuCategory:

        await category.set(update_data)
        return category


    async def soft_delete(
    self,
    category: MenuCategory,
    ) -> MenuCategory:

        await category.set(
        {
            "is_deleted": True,
            "is_active": False,
            "updated_at": datetime.now(timezone.utc),
        }
        )

        return category


    async def get_deleted_by_id(
    self,
    category_id: str,
    ) -> MenuCategory | None:

        try:
            object_id = ObjectId(category_id)
        except InvalidId:
            return None

        return await MenuCategory.find_one(
        {
            "_id": object_id,
            "is_deleted": True,
        }
        )


    async def restore(
    self,
    category: MenuCategory,
    ) -> MenuCategory:

        await category.set(
        {
            "is_deleted": False,
            "is_active": True,
            "updated_at": datetime.now(timezone.utc),
        }
        )

        return category


menu_category_repository = MenuCategoryRepository()
