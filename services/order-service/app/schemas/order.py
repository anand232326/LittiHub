from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import OrderStatus



class CreateOrderItemRequest(BaseModel):
    menu_item_id: str
    quantity: int = Field(gt=0,le=20,)


class CreateOrderRequest(BaseModel):
    restaurant_id: str
    items: list[CreateOrderItemRequest] = Field(min_length=1,)
    delivery_address: str = Field(min_length=5,max_length=500,)


class OrderItemResponse(BaseModel):
    menu_item_id: str
    name: str
    quantity: int
    unit_price: float
    total_price: float


class OrderResponse(BaseModel):
    id: str
    user_id: str
    restaurant_id: str
    items: list[OrderItemResponse]
    subtotal: float
    delivery_fee: float
    total_amount: float
    status: OrderStatus
    delivery_address: str
    created_at: datetime
    updated_at: datetime

