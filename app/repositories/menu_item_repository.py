from datetime import datetime,timezone
from bson import ObjectId
from bson.errors import InvalidId
from app.models.menu_item import MenuItem
from typing import Any
from beanie import SortDirection
from app.core.enums import (
    MenuItemSortField,
    SortOrder,
)



class MenuItemRepository:

    async def create(self,menu_item:MenuItem,)->MenuItem:
        await menu_item.insert()
        return menu_item


    async def get_by_id(self,item_id:str)->MenuItem | None:
        try:
            object_id=ObjectId(item_id)
        except InvalidId: 
            return None

        return await MenuItem.find_one(
            {
                "_id":object_id,
                "is_deleted":False
            }
        )

    async def get_all_by_restaurant(self,restaurant_id:str,is_active:bool | None=None,
            page:int=1,page_size: int = 20,search: str | None = None,
            sort_by: MenuItemSortField = MenuItemSortField.CREATED_AT,
            sort_order: SortOrder = SortOrder.DESC,category_id: str | None = None,
            is_available:bool | None=None,)->tuple[list[MenuItem], int]:
        
        query:dict[str,Any]={
            "restaurant_id":restaurant_id,
            "is_deleted":False,
        }

        if search: 
            query["name"] = {
                "$regex": search,
               "$options": "i", 

            }

        if category_id is not None: 
            query["category_id"] = category_id

        if is_active is not None:
            query["is_active"]=is_active

        if is_available is not None:
            query["is_available"]=is_available

        total = await MenuItem.find(query).count()   
        skip = (page - 1) * page_size 

        sort_direction = (
            SortDirection.ASCENDING
            if sort_order == SortOrder.ASC
            else SortDirection.DESCENDING
        )

        menu_items = await (
            MenuItem.find(query)
            .sort(
                (
                    sort_by.value,
                    sort_direction,
                )
            )
            .skip(skip)
            .limit(page_size)
            .to_list()
        )

        return menu_items, total

      

    async def get_all_by_category(
    self,
    category_id: str,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    is_active: bool | None = None,
    is_available: bool | None = None,
    sort_by: MenuItemSortField = MenuItemSortField.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC,
    ) -> tuple[list[MenuItem], int]:

        query: dict[str, Any] = {
        "category_id": category_id,
        "is_deleted": False,
        }

        if search:
            query["name"] = {
            "$regex": search,
            "$options": "i",
        }

        if is_active is not None:
            query["is_active"] = is_active

        if is_available is not None:
            query["is_available"] = is_available

        total = await MenuItem.find(query).count()

        skip = (page - 1) * page_size

        sort_direction = (
        SortDirection.ASCENDING
        if sort_order == SortOrder.ASC
        else SortDirection.DESCENDING
        )

        menu_items = await (
        MenuItem.find(query)
        .sort(
            (
                sort_by.value,
                sort_direction,
            )
        )
        .skip(skip)
        .limit(page_size)
        .to_list()
        )

        return menu_items, total
    


    

    async def update(self,menu_item: MenuItem,update_data: dict,) -> MenuItem:
        await menu_item.set(update_data)
        return menu_item


    async def soft_delete(self,menu_item: MenuItem,) -> MenuItem:
        await menu_item.set(
        {
            "is_deleted": True,
            "is_active": False,
            "is_available": False,
            "updated_at": datetime.now(timezone.utc),
        }
        )

        return menu_item


    async def get_deleted_by_id(self,item_id: str,) -> MenuItem | None:
        try:
            object_id = ObjectId(item_id)
        except InvalidId:
            return None

        return await MenuItem.find_one(
        {
            "_id": object_id,
            "is_deleted": True,
        }
        )


    async def restore(self,menu_item: MenuItem,) -> MenuItem:
        await menu_item.set(
        {
            "is_deleted": False,
            "is_active": True,
            "is_available": True,
            "updated_at": datetime.now(timezone.utc),
        }
        )

        return menu_item


menu_item_repository = MenuItemRepository()         