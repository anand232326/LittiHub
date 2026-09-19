from datetime import datetime, timezone

from app.models.menu_item import MenuItem
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.menu_category_repository import MenuCategoryRepository
from app.schemas.menu_item import (
    CreateMenuItemRequest,
    UpdateMenuItemRequest,
    MenuItemResponse,
)
from app.core.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)


class MenuItemService:

    def __init__(
        self,
        item_repository: MenuItemRepository,
        category_repository: MenuCategoryRepository,
    ):
        self.item_repository = item_repository
        self.category_repository = category_repository

    async def create_item(
        self,
        restaurant_id: str,
        request: CreateMenuItemRequest,
    ) -> MenuItemResponse:

        category = await self.category_repository.get_by_restaurant_and_id(
            restaurant_id=restaurant_id,
            category_id=request.category_id,
        )

        if not category:
            raise ResourceNotFoundError(
                "Menu category not found for this restaurant"
            )

        if not category.is_active:
            raise ResourceNotFoundError(
                "Cannot create an item under an inactive category"
            )

        existing_item = await self.item_repository.get_by_category_and_name(
            category_id=request.category_id,
            name=request.name,
        )

        if existing_item:
            raise ResourceAlreadyExistsError(
                "A menu item with this name already exists in this category"
            )

        item = MenuItem(
            restaurant_id=restaurant_id,
            category_id=request.category_id,
            name=request.name,
            description=request.description,
            price=request.price,
            image_url=request.image_url,
            is_vegetarian=request.is_vegetarian,
            preparation_time_minutes=request.preparation_time_minutes,
        )

        item = await self.item_repository.create(item)

        return self._to_response(item)

    async def get_item(
        self,
        restaurant_id: str,
        item_id: str,
    ) -> MenuItemResponse:

        item = await self.item_repository.get_by_restaurant_and_id(
            restaurant_id=restaurant_id,
            item_id=item_id,
        )

        if not item:
            raise ResourceNotFoundError(
                "Menu item not found"
            )

        return self._to_response(item)

    async def update_item(
        self,
        restaurant_id: str,
        item_id: str,
        request: UpdateMenuItemRequest,
    ) -> MenuItemResponse:

        item = await self.item_repository.get_by_restaurant_and_id(
            restaurant_id=restaurant_id,
            item_id=item_id,
        )

        if not item:
            raise ResourceNotFoundError(
                "Menu item not found"
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        if "category_id" in update_data:

            category = await (
                self.category_repository
                .get_by_restaurant_and_id(
                    restaurant_id=restaurant_id,
                    category_id=update_data["category_id"],
                )
            )

            if not category:
                raise ResourceNotFoundError(
                    "New menu category not found for this restaurant"
                )

            if not category.is_active:
                raise ResourceNotFoundError(
                    "Cannot move item to an inactive category"
                )

        if "name" in update_data:

            category_id = update_data.get(
                "category_id",
                item.category_id,
            )

            existing_item = (
                await self.item_repository
                .get_by_category_and_name(
                    category_id=category_id,
                    name=update_data["name"],
                )
            )

            if (
                existing_item
                and str(existing_item.id) != str(item.id)
            ):
                raise ResourceAlreadyExistsError(
                    "A menu item with this name already exists in this category"
                )

        for field, value in update_data.items():
            setattr(item, field, value)

        item.updated_at = datetime.now(timezone.utc)

        item = await self.item_repository.update(item)

        return self._to_response(item)

    async def delete_item(
        self,
        restaurant_id: str,
        item_id: str,
    ) -> MenuItemResponse:

        item = await self.item_repository.get_by_restaurant_and_id(
            restaurant_id=restaurant_id,
            item_id=item_id,
        )

        if not item:
            raise ResourceNotFoundError(
                "Menu item not found"
            )

        if not item.is_active:
            raise ResourceNotFoundError(
                "Menu item is already inactive"
            )

        item = await self.item_repository.delete(item)

        return self._to_response(item)

    async def restore_item(
        self,
        restaurant_id: str,
        item_id: str,
    ) -> MenuItemResponse:

        item = await self.item_repository.get_by_restaurant_and_id(
            restaurant_id=restaurant_id,
            item_id=item_id,
        )

        if not item:
            raise ResourceNotFoundError(
                "Menu item not found"
            )

        if item.is_active:
            raise ResourceAlreadyExistsError(
                "Menu item is already active"
            )

        item = await self.item_repository.restore(item)

        return self._to_response(item)

    @staticmethod
    def _to_response(
        item: MenuItem,
    ) -> MenuItemResponse:

        return MenuItemResponse(
            id=str(item.id),
            restaurant_id=item.restaurant_id,
            category_id=item.category_id,
            name=item.name,
            description=item.description,
            price=item.price,
            image_url=item.image_url,
            is_vegetarian=item.is_vegetarian,
            is_available=item.is_available,
            is_active=item.is_active,
            preparation_time_minutes=item.preparation_time_minutes,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )