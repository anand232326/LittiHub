from datetime import datetime, timezone

from app.models.menu_category import MenuCategory
from app.repositories.menu_category_repository import MenuCategoryRepository
from app.schemas.menu_category import (
    CreateMenuCategoryRequest,
    UpdateMenuCategoryRequest,
    MenuCategoryResponse,
)
from app.core.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)


class MenuCategoryService:

    def __init__(
        self,
        repository: MenuCategoryRepository,
    ):
        self.repository = repository

    async def create_category(
        self,
        restaurant_id: str,
        request: CreateMenuCategoryRequest,
    ) -> MenuCategoryResponse:

        existing_category = await self.repository.get_by_name(
            restaurant_id=restaurant_id,
            name=request.name,
        )

        if existing_category:
            raise ResourceAlreadyExistsError(
                "A category with this name already exists for this restaurant"
            )

        category = MenuCategory(
            restaurant_id=restaurant_id,
            name=request.name,
            description=request.description,
            display_order=request.display_order,
        )

        category = await self.repository.create(category)

        return self._to_response(category)

    async def get_category(
        self,
        restaurant_id: str,
        category_id: str,
    ) -> MenuCategoryResponse:

        category = await self.repository.get_by_restaurant_and_id(
            restaurant_id=restaurant_id,
            category_id=category_id,
        )

        if not category:
            raise ResourceNotFoundError(
                "Menu category not found"
            )

        return self._to_response(category)

    async def update_category(
        self,
        restaurant_id: str,
        category_id: str,
        request: UpdateMenuCategoryRequest,
    ) -> MenuCategoryResponse:

        category = await self.repository.get_by_restaurant_and_id(
            restaurant_id=restaurant_id,
            category_id=category_id,
        )

        if not category:
            raise ResourceNotFoundError(
                "Menu category not found"
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            existing_category = await self.repository.get_by_name(
                restaurant_id=restaurant_id,
                name=update_data["name"],
            )

            if (
                existing_category
                and str(existing_category.id) != str(category.id)
            ):
                raise ResourceAlreadyExistsError(
                    "A category with this name already exists for this restaurant"
                )

        for field, value in update_data.items():
            setattr(category, field, value)

        category.updated_at = datetime.now(timezone.utc)

        category = await self.repository.update(category)

        return self._to_response(category)

    async def delete_category(
        self,
        restaurant_id: str,
        category_id: str,
    ) -> MenuCategoryResponse:

        category = await self.repository.get_by_restaurant_and_id(
            restaurant_id=restaurant_id,
            category_id=category_id,
        )

        if not category:
            raise ResourceNotFoundError(
                "Menu category not found"
            )

        if not category.is_active:
            raise ResourceNotFoundError(
                "Menu category is already inactive"
            )

        category = await self.repository.delete(category)

        return self._to_response(category)

    async def restore_category(
        self,
        restaurant_id: str,
        category_id: str,
    ) -> MenuCategoryResponse:

        category = await self.repository.get_by_restaurant_and_id(
            restaurant_id=restaurant_id,
            category_id=category_id,
        )

        if not category:
            raise ResourceNotFoundError(
                "Menu category not found"
            )

        if category.is_active:
            raise ResourceAlreadyExistsError(
                "Menu category is already active"
            )

        category = await self.repository.restore(category)

        return self._to_response(category)

    @staticmethod
    def _to_response(
        category: MenuCategory,
    ) -> MenuCategoryResponse:

        return MenuCategoryResponse(
            id=str(category.id),
            restaurant_id=category.restaurant_id,
            name=category.name,
            description=category.description,
            display_order=category.display_order,
            is_active=category.is_active,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )