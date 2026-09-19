from app.schemas.menu_item import (
    CreateMenuItemRequest,
    UpdateMenuItemRequest,
    MenuItemResponse,
)
from app.services.menu_item_service import MenuItemService


class MenuItemController:

    def __init__(
        self,
        service: MenuItemService,
    ):
        self.service = service

    async def create_item(
        self,
        restaurant_id: str,category_id: str,
        request: CreateMenuItemRequest,
    ) -> MenuItemResponse:

        return await self.service.create_item(
            restaurant_id=restaurant_id,
            category_id=category_id,
            request=request,
        )

    async def get_item(
        self,
        restaurant_id: str,
        item_id: str,
    ) -> MenuItemResponse:

        return await self.service.get_item(
            restaurant_id=restaurant_id,
            item_id=item_id,
        )

    async def update_item(
        self,
        restaurant_id: str,
        item_id: str,
        request: UpdateMenuItemRequest,
    ) -> MenuItemResponse:

        return await self.service.update_item(
            restaurant_id=restaurant_id,
            item_id=item_id,
            request=request,
        )

    async def delete_item(
        self,
        restaurant_id: str,
        item_id: str,
    ) -> MenuItemResponse:

        return await self.service.delete_item(
            restaurant_id=restaurant_id,
            item_id=item_id,
        )

    async def restore_item(
        self,
        restaurant_id: str,
        item_id: str,
    ) -> MenuItemResponse:

        return await self.service.restore_item(
            restaurant_id=restaurant_id,
            item_id=item_id,
        )