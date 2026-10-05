from datetime import datetime, timezone
from typing import Optional

from pymongo import ReturnDocument

from app.models.inventory import Inventory


class InventoryRepository:

    async def get_by_id(
        self,
        inventory_id: str,
    ) -> Optional[Inventory]:

        return await Inventory.get(
            inventory_id
        )

    async def get_by_menu_item(
        self,
        restaurant_id: str,
        menu_item_id: str,
    ) -> Optional[Inventory]:

        return await Inventory.find_one(
            Inventory.restaurant_id == restaurant_id,
            Inventory.menu_item_id == menu_item_id,
        )

    async def create(
        self,
        inventory: Inventory,
    ) -> Inventory:

        await inventory.insert()

        return inventory

    async def update(
        self,
        inventory: Inventory,
    ) -> Inventory:

        inventory.updated_at = datetime.now(
            timezone.utc
        )

        await inventory.save()

        return inventory

    async def reserve(
        self,
        inventory_id: str,
        quantity: int,
    ) -> Optional[Inventory]:

        collection = Inventory.get_pymongo_collection()

        document = await collection.find_one_and_update(
            {
                "_id": inventory_id,
                "$expr": {
                    "$gte": [
                        {
                            "$subtract": [
                                "$quantity",
                                "$reserved_quantity",
                            ]
                        },
                        quantity,
                    ]
                },
            },
            {
                "$inc": {
                    "reserved_quantity": quantity,
                },
                "$set": {
                    "updated_at": datetime.now(
                        timezone.utc
                    ),
                },
            },
            return_document=ReturnDocument.AFTER,
        )

        if not document:
            return None

        return Inventory.model_validate(
            document
        )

    async def release(
        self,
        inventory_id: str,
        quantity: int,
    ) -> Optional[Inventory]:

        collection = Inventory.get_pymongo_collection()

        document = await collection.find_one_and_update(
            {
                "_id": inventory_id,
                "reserved_quantity": {
                    "$gte": quantity,
                },
            },
            {
                "$inc": {
                    "reserved_quantity": -quantity,
                },
                "$set": {
                    "updated_at": datetime.now(
                        timezone.utc
                    ),
                },
            },
            return_document=ReturnDocument.AFTER,
        )

        if not document:
            return None

        return Inventory.model_validate(
            document
        )


inventory_repository = InventoryRepository()