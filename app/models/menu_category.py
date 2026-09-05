from datetime import datetime, timezone

from beanie import Document
from pydantic import Field

class MenuCategory(Document):
    restaurant_id: str
    name: str
    description: str | None = None
    is_active: bool = True
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Settings:
    name = "menu_categories"

