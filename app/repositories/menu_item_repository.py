from datetime import datetime,timezone
from bson import ObjectId
from bson.errors import InvalidId
from app.models.menu_item import MenuItem



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
            is_available:bool | None=None,)->list[MenuItem]:
        query={
            "restaurant_id":restaurant_id,
            "is_deleted":False,
        }

        if is_active is not None:
            query["is_active"]=is_active

        if is_available is not None:
            query["is_available"]=is_available

        return await(
            MenuItem.find(query)
            .to_list()
        )  


    async def get_all_by_category(
    self,
    category_id: str,
    is_active: bool | None = None,
    is_available: bool | None = None,
    ) -> list[MenuItem]:

        query = {
        "category_id": category_id,
        "is_deleted": False,
        }

        if is_active is not None:
            query["is_active"] = is_active

        if is_available is not None:
            query["is_available"] = is_available

        return await (
        MenuItem.find(query)
        .to_list()
        )


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