
from app.core.enums import OrderStatus
from app.schemas.order import (
    CreateOrderRequest,
    OrderResponse,
)
from app.services.order_service import order_service


class OrderController:

    async def create_order(
        self,
        user_id: str,
        request: CreateOrderRequest,
    ) -> OrderResponse:

        return await order_service.create_order(
            user_id=user_id,
            request=request,
        )

    async def get_my_orders(
        self,
        user_id: str,
    ) -> list[OrderResponse]:

        return await order_service.get_my_orders(
            user_id=user_id,
        )

    async def get_order_by_id(
        self,
        order_id: str,
        user_id: str,
    ) -> OrderResponse:

        return await order_service.get_order_by_id(
            order_id=order_id,
            user_id=user_id,
        )

    async def update_order_status(
        self,
        order_id: str,
        user_id: str,
        role: str | None,
        new_status: OrderStatus,
    ) -> OrderResponse:

        return await order_service.update_order_status(
            order_id=order_id,
            user_id=user_id,
            role=role,
            new_status=new_status,
        )


order_controller = OrderController()

