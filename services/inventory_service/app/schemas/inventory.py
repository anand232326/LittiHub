from datetime import datetime

from pydantic import BaseModel, Field


class CreateInventoryRequest(BaseModel):
    restaurant_id: str = Field(min_length=1,)
    menu_item_id: str = Field(min_length=1,)
    quantity: int = Field(ge=0,)


class UpdateInventoryRequest(BaseModel):

    quantity: int = Field(
        ge=0,
    )


class InventoryResponse(BaseModel):
    id: str
    restaurant_id: str
    menu_item_id: str
    quantity: int
    reserved_quantity: int
    available_quantity: int
    created_at: datetime
    updated_at: datetime