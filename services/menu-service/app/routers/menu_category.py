from fastapi import APIRouter, Depends, status

from app.controllers.menu_category_controller import MenuCategoryController
from app.dependencies.menu import get_menu_category_controller
from app.schemas.menu_category import (
    CreateMenuCategoryRequest,
    UpdateMenuCategoryRequest,
    MenuCategoryResponse,
)

router = APIRouter(
    prefix="/restaurants/{restaurant_id}/categories",
    tags=["Menu Categories"],
)


@router.post(
    "",
    response_model=MenuCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    restaurant_id: str,
    request: CreateMenuCategoryRequest,
    controller: MenuCategoryController = Depends(
        get_menu_category_controller
    ),
):
    return await controller.create_category(
        restaurant_id=restaurant_id,
        request=request,
    )


@router.get(
    "/{category_id}",
    response_model=MenuCategoryResponse,
)
async def get_category(
    restaurant_id: str,
    category_id: str,
    controller: MenuCategoryController = Depends(
        get_menu_category_controller
    ),
):
    return await controller.get_category(
        restaurant_id=restaurant_id,
        category_id=category_id,
    )


@router.patch(
    "/{category_id}",
    response_model=MenuCategoryResponse,
)
async def update_category(
    restaurant_id: str,
    category_id: str,
    request: UpdateMenuCategoryRequest,
    controller: MenuCategoryController = Depends(
        get_menu_category_controller
    ),
):
    return await controller.update_category(
        restaurant_id=restaurant_id,
        category_id=category_id,
        request=request,
    )


@router.delete(
    "/{category_id}",
    response_model=MenuCategoryResponse,
)
async def delete_category(
    restaurant_id: str,
    category_id: str,
    controller: MenuCategoryController = Depends(
        get_menu_category_controller
    ),
):
    return await controller.delete_category(
        restaurant_id=restaurant_id,
        category_id=category_id,
    )


@router.post(
    "/{category_id}/restore",
    response_model=MenuCategoryResponse,
)
async def restore_category(
    restaurant_id: str,
    category_id: str,
    controller: MenuCategoryController = Depends(
        get_menu_category_controller
    ),
):
    return await controller.restore_category(
        restaurant_id=restaurant_id,
        category_id=category_id,
    )