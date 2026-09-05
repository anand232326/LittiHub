from fastapi import APIRouter, Depends, Query, status
from app.controllers.menu_category_controller import (
menu_category_controller,
)
from app.core.enums import UserRole
from app.dependencies.auth import require_role
from app.schemas.menu_category import (
MenuCategoryCreate,
MenuCategoryResponse,
MenuCategoryUpdate,
)

router = APIRouter(
prefix="/menu-categories",
tags=["Menu Categories"],
)

# CUSTOMER + ADMIN

@router.get("/restaurant/{restaurant_id}",response_model=list[MenuCategoryResponse],)
async def get_restaurant_categories(restaurant_id: str,is_active: bool | None = Query(default=None),):
    return await menu_category_controller.get_all_by_restaurant(
    restaurant_id=restaurant_id,
    is_active=is_active,
    )

# CUSTOMER + ADMIN

@router.get("/{category_id}",response_model=MenuCategoryResponse,)
async def get_category(category_id: str,):
    return await menu_category_controller.get_by_id(category_id=category_id,
    )

# ADMIN ONLY

@router.post("/",response_model=MenuCategoryResponse,)
async def create_category(category_data: MenuCategoryCreate,_: object = Depends(require_role(UserRole.ADMIN)),):
    return await menu_category_controller.create(
    category_data=category_data,
    )

# ADMIN ONLY

@router.patch("/{category_id}",response_model=MenuCategoryResponse,)
async def update_category(category_id: str,category_data: MenuCategoryUpdate,_: object = Depends(require_role(UserRole.ADMIN)),):
    return await menu_category_controller.update(
    category_id=category_id,
    category_data=category_data,
    )

# ADMIN ONLY

@router.delete("/{category_id}",status_code=status.HTTP_204_NO_CONTENT,)
async def delete_category(category_id: str,_: object = Depends(require_role(UserRole.ADMIN)),):
    await menu_category_controller.delete(
    category_id=category_id,
    )

# ADMIN ONLY

@router.patch("/{category_id}/restore",response_model=MenuCategoryResponse,)
async def restore_category(category_id: str,_: object = Depends(require_role(UserRole.ADMIN)),):
    return await menu_category_controller.restore(
    category_id=category_id,
    )
