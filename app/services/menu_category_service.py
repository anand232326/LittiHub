from datetime import datetime, timezone

from app.models.menu_category import MenuCategory
from app.repositories.menu_category_repository import (
menu_category_repository,
)
from app.repositories.restaurant_repository import (
restaurant_repository,
)
from app.schemas.menu_category import (
MenuCategoryCreate,
MenuCategoryResponse,
MenuCategoryUpdate,
)

class MenuCategoryService:


    def __init__(self):
        self.menu_category_repository = menu_category_repository
        self.restaurant_repository = restaurant_repository


    async def create(
    self,
    category_data: MenuCategoryCreate,
    ) -> MenuCategoryResponse | None:

        # Validate that the restaurant exists
        restaurant = await self.restaurant_repository.get_by_id(
        category_data.restaurant_id
        )

        if restaurant is None:
            return None

        category = MenuCategory(
        restaurant_id=category_data.restaurant_id,
        name=category_data.name,
        description=category_data.description,
        )

        category = await self.menu_category_repository.create(
        category
        )

        return self._to_response(category)


    async def get_by_id(
    self,
    category_id: str,
    ) -> MenuCategoryResponse | None:

        category = await self.menu_category_repository.get_by_id(
        category_id
        )

        if category is None:
            return None

        return self._to_response(category)


    async def get_all_by_restaurant(
    self,
    restaurant_id: str,
    is_active: bool | None = None,
    ) -> list[MenuCategoryResponse]:

        categories = (
        await self.menu_category_repository.get_all_by_restaurant(
            restaurant_id=restaurant_id,
            is_active=is_active,
        )
        )

        return [
        self._to_response(category)
        for category in categories
        ]


    async def update(
    self,
    category_id: str,
    category_data: MenuCategoryUpdate,
    ) -> MenuCategoryResponse | None:

        category = await self.menu_category_repository.get_by_id(
        category_id
        )

        if category is None:
            return None

        update_data = category_data.model_dump(
        exclude_unset=True
        )

        if not update_data:
            return self._to_response(category)

        update_data["updated_at"] = datetime.now(
        timezone.utc
        )

        category = await self.menu_category_repository.update(
        category,
        update_data,
        )

        return self._to_response(category)


    async def delete(
    self,
    category_id: str,
    ) -> bool:

        category = await self.menu_category_repository.get_by_id(
        category_id
        )

        if category is None:
            return False

        await self.menu_category_repository.soft_delete(
        category
        )

        return True


    async def restore(
    self,
    category_id: str,
    ) -> MenuCategoryResponse | None:

        category = (
        await self.menu_category_repository.get_deleted_by_id(
            category_id
        )
        )

        if category is None:
            return None

        category = await self.menu_category_repository.restore(
        category
        )

        return self._to_response(category)


    def _to_response(
    self,
    category: MenuCategory,
    ) -> MenuCategoryResponse:

        return MenuCategoryResponse(
        id=str(category.id),
        restaurant_id=category.restaurant_id,
        name=category.name,
        description=category.description,
        is_active=category.is_active,
        created_at=category.created_at,
        updated_at=category.updated_at,
        )



menu_category_service = MenuCategoryService()
