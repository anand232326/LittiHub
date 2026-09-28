from typing import Any
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


class CartCheckoutResponse(BaseModel):
    user_id: str
    restaurant_id: str
    items: list[Any] = []  # You can replace Any with a specific Item schema later
    subtotal: float
    total_items: int