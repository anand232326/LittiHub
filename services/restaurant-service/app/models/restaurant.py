
from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Restaurant(Document):

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    slug: str = Field(
        min_length=2,
        max_length=120,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    phone: str | None = None

    email: str | None = None

    address: str = Field(
        min_length=5,
        max_length=250,
    )

    city: str = Field(
        min_length=2,
        max_length=100,
    )

    state: str = Field(
        min_length=2,
        max_length=100,
    )

    pincode: str = Field(
        min_length=4,
        max_length=10,
    )

    latitude: float | None = None

    longitude: float | None = None

    is_active: bool = True

    is_open: bool = False

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class Settings:
    name = "restaurants"

    indexes = [
        "name",
        "city",
        "is_active",
        "is_open",
        {
            "key": [
                ("slug", 1),
            ],
            "unique": True,
        },
    ]

