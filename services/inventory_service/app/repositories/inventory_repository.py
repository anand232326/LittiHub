from app.models.inventory import Inventory




class InventoryRepository:

    async def create(self,inventory: Inventory,) -> Inventory:
        await inventory.insert()
        return inventory



    async def get_by_id(self,inventory_id: str,) -> Inventory | None:
        return await Inventory.get(
            inventory_id
        )




    async def get_by_restaurant_and_menu_item(self,restaurant_id: str,menu_item_id: str,) -> Inventory | None:
        return await Inventory.find_one(
            {
                "restaurant_id": restaurant_id,
                "menu_item_id": menu_item_id,
            }
        )





    async def update(self,inventory: Inventory,) -> Inventory:
        await inventory.save()
        return inventory





    async def delete(self,inventory: Inventory,) -> None:
        await inventory.delete()




inventory_repository = InventoryRepository()