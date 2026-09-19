from app.controllers.menu_category_controller import MenuCategoryController
from app.controllers.menu_item_controller import MenuItemController
from app.repositories.menu_category_repository import MenuCategoryRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.services.menu_category_service import MenuCategoryService
from app.services.menu_item_service import MenuItemService


def get_menu_category_controller() -> MenuCategoryController:

    repository = MenuCategoryRepository()

    service = MenuCategoryService(
        repository=repository,
    )

    return MenuCategoryController(
        service=service,
    )


def get_menu_item_controller() -> MenuItemController:

    item_repository = MenuItemRepository()
    category_repository = MenuCategoryRepository()

    service = MenuItemService(
        item_repository=item_repository,
        category_repository=category_repository,
    )

    return MenuItemController(
        service=service,
    )