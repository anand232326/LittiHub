from datetime import datetime, timezone

from beanie import Document
from pymongo import ASCENDING, IndexModel
from pydantic import Field


class Inventory(Document):

    restaurant_id: str
    menu_item_id: str
    quantity: int = Field(
        default=0,
        ge=0,
    )

    reserved_quantity: int = Field(
        default=0,
        ge=0,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "inventory"
        indexes = [
            IndexModel(
                [("restaurant_id", ASCENDING), ("menu_item_id", ASCENDING)],
                unique=True,
            )
        ]

    @property
    def available_quantity(self) -> int:
        return self.quantity - self.reserved_quantity