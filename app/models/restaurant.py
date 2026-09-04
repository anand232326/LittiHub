from datetime import datetime, timezone
from beanie import Document
from pydantic import Field


class Restaurant(Document):

    outlet_name: str = Field(min_length=2,max_length=100,)
    phone: str = Field(min_length=10,max_length=15,)
    address: str = Field(min_length=5,max_length=300,)
    city: str = Field(min_length=2,max_length=100,)
    locality: str = Field(min_length=2,max_length=100,)
    pincode: str = Field(min_length=6,max_length=10,)
    latitude: float | None = None
    longitude: float | None = None
    owner_id: str
    is_active: bool = True
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "restaurants"