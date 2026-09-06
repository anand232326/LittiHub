from datetime import datetime,timezone
from beanie import Document,PydanticObjectId
from pydantic import Field
from typing import Optional


class MenuItem(Document):
    restaurant_id:str
    category_id:str
    name:str
    description_id:Optional[PydanticObjectId] = None
    price:float
    is_available:bool=True
    is_active:bool=True
    is_deleted:bool=False
    image_url:str | None=None
    created_at:datetime=Field(
        default_factory=lambda:datetime.now(timezone.utc)
    )
    updated_at:datetime=Field(
        default_factory=lambda:datetime.now(timezone.utc)
    )



class Settings: 
    name = "menu_items"    