from datetime import datetime, timezone
from beanie import Document
from pydantic import Field


class MenuCategory(Document):

    restaurant_id: str = Field(min_length=1)
    name: str = Field(min_length=2,max_length=100,)
    description: str | None = Field(default=None,max_length=500,)
    display_order: int = Field(default=0,ge=0,)
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



    class Settings:

        name = "menu_categories"

        indexes = [
            "restaurant_id",
            "name",
            "is_active",
            "display_order",
        ]