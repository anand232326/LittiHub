from fastapi import HTTPException, status
from app.schemas.menu_category import (
MenuCategoryCreate,
MenuCategoryResponse,
MenuCategoryUpdate,
)
from app.services.menu_category_service import (
menu_category_service,
)

class MenuCategoryController:


    async def create(
    self,
    category_data: MenuCategoryCreate,
    ) -> MenuCategoryResponse:

        category = await menu_category_service.create(
        category_data=category_data,
        )

        if category is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Restaurant with id "
                f"'{category_data.restaurant_id}' not found"
            ),
            )

        return category


    async def get_by_id(
    self,
    category_id: str,
    ) -> MenuCategoryResponse:

        category = await menu_category_service.get_by_id(
        category_id=category_id,
        )

        if category is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Menu category with id "
                f"'{category_id}' not found"
            ),
            )

        return category


    async def get_all_by_restaurant(
    self,
    restaurant_id: str,
    is_active: bool | None = None,
    ) -> list[MenuCategoryResponse]:

        return await menu_category_service.get_all_by_restaurant(
        restaurant_id=restaurant_id,
        is_active=is_active,
        )


    async def update(
    self,
    category_id: str,
    category_data: MenuCategoryUpdate,
    ) -> MenuCategoryResponse:

        category = await menu_category_service.update(
        category_id=category_id,
        category_data=category_data,
        )

        if category is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Menu category with id "
                f"'{category_id}' not found"
            ),
            )

        return category


    async def delete(
    self,
    category_id: str,
    ) -> None:

        deleted = await menu_category_service.delete(
        category_id=category_id,
        )

        if not deleted:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Menu category with id "
                f"'{category_id}' not found"
            ),
            )


    async def restore(
    self,
    category_id: str,
    ) -> MenuCategoryResponse:

        category = await menu_category_service.restore(
        category_id=category_id,
        )

        if category is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Deleted menu category with id "
                f"'{category_id}' not found"
            ),
            )

        return category
    

menu_category_controller = MenuCategoryController()
