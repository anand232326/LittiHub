from typing import Optional

from app.models.menu_category import MenuCategory


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
    ) -> Optional[MenuCategory]:

        return await MenuCategory.get(
            category_id
        )

    async def get_by_restaurant_and_id(
        self,
        restaurant_id: str,
        category_id: str,
    ) -> Optional[MenuCategory]:

        return await MenuCategory.find_one(
            MenuCategory.id == category_id,
            MenuCategory.restaurant_id == restaurant_id,
        )

    async def get_by_name(
        self,
        restaurant_id: str,
        name: str,
    ) -> Optional[MenuCategory]:

        return await MenuCategory.find_one(
            MenuCategory.restaurant_id == restaurant_id,
            MenuCategory.name == name,
        )

    async def update(
        self,
        category: MenuCategory,
    ) -> MenuCategory:

        await category.save()

        return category

    async def delete(
        self,
        category: MenuCategory,
    ) -> MenuCategory:

        category.is_active = False

        await category.save()

        return category