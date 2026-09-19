from app.schemas.menu_category import (
    CreateMenuCategoryRequest,
    UpdateMenuCategoryRequest,
    MenuCategoryResponse,
)
from app.services.menu_category_service import MenuCategoryService


class MenuCategoryController:

    def __init__(
        self,
        service: MenuCategoryService,
    ):
        self.service = service

    async def create_category(
        self,
        restaurant_id: str,
        request: CreateMenuCategoryRequest,
    ) -> MenuCategoryResponse:

        return await self.service.create_category(
            restaurant_id=restaurant_id,
            request=request,
        )

    async def get_category(
        self,
        restaurant_id: str,
        category_id: str,
    ) -> MenuCategoryResponse:

        return await self.service.get_category(
            restaurant_id=restaurant_id,
            category_id=category_id,
        )

    async def update_category(
        self,
        restaurant_id: str,
        category_id: str,
        request: UpdateMenuCategoryRequest,
    ) -> MenuCategoryResponse:

        return await self.service.update_category(
            restaurant_id=restaurant_id,
            category_id=category_id,
            request=request,
        )

    async def delete_category(
        self,
        restaurant_id: str,
        category_id: str,
    ) -> MenuCategoryResponse:

        return await self.service.delete_category(
            restaurant_id=restaurant_id,
            category_id=category_id,
        )

    async def restore_category(
        self,
        restaurant_id: str,
        category_id: str,
    ) -> MenuCategoryResponse:

        return await self.service.restore_category(
            restaurant_id=restaurant_id,
            category_id=category_id,
        )