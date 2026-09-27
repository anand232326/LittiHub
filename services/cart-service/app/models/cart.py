
from pydantic import BaseModel, Field


class CartItem(BaseModel):
    menu_item_id: str
    name: str
    price: float = Field(
        ge=0
    )
    quantity: int = Field(
        gt=0
    )
    total_price: float = Field(
        ge=0
    )


class Cart(BaseModel):
    user_id: str
    restaurant_id: str | None = None
    items: list[CartItem] = Field(
        default_factory=list
    )
    subtotal: float = Field(
        default=0.0,
        ge=0,
    )
    total_items: int = Field(
        default=0,
        ge=0,
    )
