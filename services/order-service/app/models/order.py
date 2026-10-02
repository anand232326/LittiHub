
from datetime import datetime, timezone
from pymongo import IndexModel
from beanie import Document
from pydantic import BaseModel, Field

from app.core.enums import OrderStatus


class OrderItem(BaseModel):
    menu_item_id: str
    name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    total_price: float = Field(gt=0)


class Order(Document):
    user_id: str
    restaurant_id: str

    # Idempotency
    idempotency_key: str
    idempotency_request_hash: str

    items: list[OrderItem]

    subtotal: float = Field(gt=0)
    delivery_fee: float = Field(ge=0)
    total_amount: float = Field(gt=0)

    status: OrderStatus = OrderStatus.PENDING

    delivery_address: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "orders"
        indexes = [
            IndexModel(
                [
                    ("user_id", 1),
                    ("idempotency_key", 1),
                ],
                unique=True,
            )
        ]

