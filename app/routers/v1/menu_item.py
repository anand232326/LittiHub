from fastapi import APIRouter, Depends, Query, status
from app.controllers.menu_item_controller import menu_item_controller
from app.core.enums import UserRole
from app.dependencies.auth import require_role
from app.schemas.menu_item import (MenuItemCreate,MenuItemResponse,MenuItemUpdate,
                                   MenuItemListResponse)
from app.core.enums import (
    MenuItemSortField,
    SortOrder,
)




router = APIRouter(
prefix="/menu-items",
tags=["Menu Items"],
)



@router.get("/restaurant/{restaurant_id}",response_model=MenuItemListResponse,)
async def get_restaurant_items(restaurant_id: str,
    page: int = Query(default=1,ge=1,),
    page_size: int = Query(default=20,ge=1,le=100,),
    search: str | None = Query(default=None,min_length=1,),
    category_id: str | None = Query(default=None,),
    is_active: bool | None = Query(default=None,),
    is_available: bool | None = Query(default=None,),
    sort_by: MenuItemSortField = Query(default=MenuItemSortField.CREATED_AT,),
    sort_order: SortOrder = Query(default=SortOrder.DESC,),):


    return await menu_item_controller.get_all_by_restaurant(
        restaurant_id=restaurant_id,
        page=page,
        page_size=page_size,
        search=search,
        category_id=category_id,
        is_active=is_active,
        is_available=is_available,
        sort_by=sort_by,
        sort_order=sort_order,
    )




@router.get("/category/{category_id}",response_model=list[MenuItemResponse],)
async def get_category_items(category_id: str,is_active: bool | None = Query(default=None),
    is_available: bool | None = Query(default=None),):

    return await menu_item_controller.get_all_by_category(
    category_id=category_id,
    is_active=is_active,
    is_available=is_available,
    )



@router.post("/",response_model=MenuItemResponse,status_code=status.HTTP_201_CREATED,)
async def create_menu_item(item_data: MenuItemCreate,_: object = Depends(require_role(UserRole.ADMIN)),):
    return await menu_item_controller.create(
    item_data=item_data,
    )


@router.get("/{item_id}",response_model=MenuItemResponse,)
async def get_menu_item(item_id: str,):
    return await menu_item_controller.get_by_id(
    item_id=item_id,
    )



@router.patch("/{item_id}",response_model=MenuItemResponse,)
async def update_menu_item(item_id: str,item_data: MenuItemUpdate,_: object = Depends(require_role(UserRole.ADMIN)),):
    return await menu_item_controller.update(
    item_id=item_id,
    item_data=item_data,
    )



@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT,)
async def delete_menu_item(item_id: str,_: object = Depends(require_role(UserRole.ADMIN)),):
    await menu_item_controller.delete(
    item_id=item_id,
    )



@router.patch("/{item_id}/restore",response_model=MenuItemResponse,)
async def restore_menu_item(item_id: str,_: object = Depends(require_role(UserRole.ADMIN)),):
    return await menu_item_controller.restore(
    item_id=item_id,
    )
