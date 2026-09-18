from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class MenuItem(Document):

    restaurant_id: str = Field(
        min_length=1
    )

    category_id: str = Field(
        min_length=1
    )

    name: str = Field(
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    price: float = Field(
        gt=0
    )

    image_url: str | None = None

    is_vegetarian: bool = True

    is_available: bool = True

    is_active: bool = True

    preparation_time_minutes: int = Field(
        default=15,
        ge=1,
        le=180,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:

        name = "menu_items"

        indexes = [
            "restaurant_id",
            "category_id",
            "name",
            "is_available",
            "is_active",
        ]