
from pydantic import BaseModel, Field


class AddCartItemRequest(BaseModel):
    restaurant_id: str
    menu_item_id: str
    quantity: int = Field(
        gt=0,
        le=20,
    )


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(
        gt=0,
        le=20,
    )


class CartItemResponse(BaseModel):
    menu_item_id: str
    name: str
    price: float
    quantity: int
    total_price: float


class CartResponse(BaseModel):
    user_id: str
    restaurant_id: str | None = None
    items: list[CartItemResponse]
    subtotal: float
    total_items: int

