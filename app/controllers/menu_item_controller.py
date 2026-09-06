from fastapi import HTTPException, status
from app.schemas.menu_item import MenuItemCreate,MenuItemResponse,MenuItemUpdate
from app.services.menu_item_service import menu_item_service





class MenuItemController:


    async def create(self,item_data: MenuItemCreate,) -> MenuItemResponse:
        menu_item = await menu_item_service.create(
        item_data=item_data,
        )

        if menu_item is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid restaurant or category. "
                "Make sure the category belongs to the restaurant."
            ),
        )

        return menu_item


    async def get_by_id(self,item_id: str,) -> MenuItemResponse:

        menu_item = await menu_item_service.get_by_id(
        item_id=item_id,
        )

        if menu_item is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Menu item with id "
                f"'{item_id}' not found"
            ),
        )

        return menu_item


    async def get_all_by_restaurant(
    self,
    restaurant_id: str,
    is_active: bool | None = None,
    is_available: bool | None = None,
    ) -> list[MenuItemResponse]:

        return await menu_item_service.get_all_by_restaurant(
        restaurant_id=restaurant_id,
        is_active=is_active,
        is_available=is_available,
        )


    async def get_all_by_category(
    self,
    category_id: str,
    is_active: bool | None = None,
    is_available: bool | None = None,
    ) -> list[MenuItemResponse]:

        return await menu_item_service.get_all_by_category(
        category_id=category_id,
        is_active=is_active,
        is_available=is_available,
        )


    async def update(
    self,
    item_id: str,
    item_data: MenuItemUpdate,
    ) -> MenuItemResponse:

        menu_item = await menu_item_service.update(
        item_id=item_id,
        item_data=item_data,
    )

        if menu_item is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Menu item with id "
                f"'{item_id}' not found"
            ),
        )

        return menu_item


    async def delete(
    self,
    item_id: str,
    ) -> None:

        deleted = await menu_item_service.delete(
        item_id=item_id,
        )

        if not deleted:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Menu item with id "
                f"'{item_id}' not found"
            ),
        )


    async def restore(
    self,
    item_id: str,
    ) -> MenuItemResponse:

        menu_item = await menu_item_service.restore(
        item_id=item_id,
        )

        if menu_item is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Deleted menu item with id "
                f"'{item_id}' not found"
            ),
        )

        return menu_item


menu_item_controller = MenuItemController()
