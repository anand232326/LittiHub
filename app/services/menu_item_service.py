from datetime import datetime, timezone
from app.models.menu_item import MenuItem
from app.repositories.menu_category_repository import menu_category_repository
from app.repositories.menu_item_repository import menu_item_repository
from app.repositories.restaurant_repository import restaurant_repository
from app.schemas.menu_item import MenuItemCreate, MenuItemResponse, MenuItemUpdate


class MenuItemService:

    def __init__(self):
        self.menu_item_repository = menu_item_repository
        self.restaurant_repository = restaurant_repository
        self.menu_category_repository = menu_category_repository

    async def create(
        self,
        item_data: MenuItemCreate,
    ) -> MenuItemResponse | None:
        # 1. Validate restaurant
        restaurant = await self.restaurant_repository.get_by_id(
            item_data.restaurant_id
        )
        if restaurant is None:
            return None

        # 2. Validate category
        category = await self.menu_category_repository.get_by_id(
            item_data.category_id
        )
        if category is None:
            return None

        # 3. Validate category belongs to restaurant
        if category.restaurant_id != item_data.restaurant_id:
            return None

        # 4. Create menu item document
        # Ensure description / description_id attributes match your Beanie model
        menu_item = MenuItem(
            restaurant_id=item_data.restaurant_id,
            category_id=item_data.category_id,
            name=item_data.name,
            description=getattr(item_data, "description", None),
            description_id=getattr(item_data, "description_id", None),
            price=item_data.price,
            image_url=item_data.image_url,
        )

        menu_item = await self.menu_item_repository.create(menu_item)
        return self._to_response(menu_item)

    async def get_by_id(
        self,
        item_id: str,
    ) -> MenuItemResponse | None:
        menu_item = await self.menu_item_repository.get_by_id(item_id)
        if menu_item is None:
            return None
        return self._to_response(menu_item)

    async def get_all_by_restaurant(
        self,
        restaurant_id: str,
        is_active: bool | None = None,
        is_available: bool | None = None,
    ) -> list[MenuItemResponse]:
        menu_items = await self.menu_item_repository.get_all_by_restaurant(
            restaurant_id=restaurant_id,
            is_active=is_active,
            is_available=is_available,
        )
        return [self._to_response(menu_item) for menu_item in menu_items]

    async def get_all_by_category(
        self,
        category_id: str,
        is_active: bool | None = None,
        is_available: bool | None = None,
    ) -> list[MenuItemResponse]:
        menu_items = await self.menu_item_repository.get_all_by_category(
            category_id=category_id,
            is_active=is_active,
            is_available=is_available,
        )
        return [self._to_response(menu_item) for menu_item in menu_items]

    async def update(
        self,
        item_id: str,
        item_data: MenuItemUpdate,
    ) -> MenuItemResponse | None:
        menu_item = await self.menu_item_repository.get_by_id(item_id)
        if menu_item is None:
            return None

        update_data = item_data.model_dump(exclude_unset=True)
        if not update_data:
            return self._to_response(menu_item)

        update_data["updated_at"] = datetime.now(timezone.utc)

        menu_item = await self.menu_item_repository.update(
            menu_item,
            update_data,
        )
        return self._to_response(menu_item)

    async def delete(
        self,
        item_id: str,
    ) -> bool:
        menu_item = await self.menu_item_repository.get_by_id(item_id)
        if menu_item is None:
            return False

        await self.menu_item_repository.soft_delete(menu_item)
        return True

    async def restore(
        self,
        item_id: str,
    ) -> MenuItemResponse | None:
        menu_item = await self.menu_item_repository.get_deleted_by_id(item_id)
        if menu_item is None:
            return None

        menu_item = await self.menu_item_repository.restore(menu_item)
        return self._to_response(menu_item)

    def _to_response(
        self,
        menu_item: MenuItem,
    ) -> MenuItemResponse:

        # Safely extract description text or description_id reference
        description_value = getattr(
            menu_item,
            "description",
            getattr(menu_item, "description_id", None),
        )

        return MenuItemResponse(
            id=str(menu_item.id),
            restaurant_id=str(menu_item.restaurant_id),
            category_id=str(menu_item.category_id),
            name=menu_item.name,
            description=description_value,
            price=menu_item.price,
            image_url=menu_item.image_url,
            is_available=menu_item.is_available,
            is_active=menu_item.is_active,
            created_at=menu_item.created_at,
            updated_at=menu_item.updated_at,
        )


menu_item_service = MenuItemService()