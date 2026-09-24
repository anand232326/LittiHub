
from app.clients.menu_client import menu_client
from app.clients.restaurant_client import restaurant_client
from app.clients.user_client import user_client
from app.core.enums import OrderStatus
from app.core.exceptions import (
    InvalidRequestError,
    PermissionDeniedError,
    ResourceNotFoundError,
)
from app.models.order import Order, OrderItem
from app.repositories.order_repository import (
    order_repository,
)
from app.schemas.order import (
    CreateOrderRequest,
    OrderResponse,
)


class OrderService:

    async def create_order(
        self,
        user_id: str,
        request: CreateOrderRequest,
    ) -> OrderResponse:

        user = await user_client.get_user(
            user_id=user_id
        )

        if user is None:
            raise ResourceNotFoundError(
                "User not found"
            )

        restaurant = await restaurant_client.get_restaurant(
            restaurant_id=request.restaurant_id
        )

        if restaurant is None:
            raise ResourceNotFoundError(
                "Restaurant not found"
            )

        if not restaurant.get(
            "is_active",
            False,
        ):
            raise InvalidRequestError(
                "Restaurant is not active"
            )

        if not restaurant.get(
            "is_open",
            False,
        ):
            raise InvalidRequestError(
                "Restaurant is currently closed"
            )

        order_items: list[OrderItem] = []
        subtotal = 0.0

        for requested_item in request.items:

            menu_item = await menu_client.get_menu_item(
                restaurant_id=request.restaurant_id,
                item_id=requested_item.menu_item_id,
            )

            if menu_item is None:
                raise ResourceNotFoundError(
                    f"Menu item "
                    f"'{requested_item.menu_item_id}' "
                    f"not found"
                )

            if (
                menu_item.get("restaurant_id")
                != request.restaurant_id
            ):
                raise InvalidRequestError(
                    "Menu item does not belong "
                    "to this restaurant"
                )

            if not menu_item.get(
                "is_active",
                False,
            ):
                raise InvalidRequestError(
                    f"Menu item "
                    f"'{menu_item.get('name')}' "
                    f"is inactive"
                )

            if not menu_item.get(
                "is_available",
                False,
            ):
                raise InvalidRequestError(
                    f"Menu item "
                    f"'{menu_item.get('name')}' "
                    f"is currently unavailable"
                )

            unit_price = float(
                menu_item["price"]
            )

            quantity = requested_item.quantity

            item_total = (
                unit_price * quantity
            )

            order_item = OrderItem(
                menu_item_id=menu_item["id"],
                name=menu_item["name"],
                quantity=quantity,
                unit_price=unit_price,
                total_price=item_total,
            )

            order_items.append(
                order_item
            )

            subtotal += item_total

        delivery_fee = (
            self._calculate_delivery_fee(
                subtotal=subtotal
            )
        )

        total_amount = (
            subtotal + delivery_fee
        )

        order = Order(
            user_id=user_id,
            restaurant_id=request.restaurant_id,
            items=order_items,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
            delivery_address=request.delivery_address,
        )

        order = await order_repository.create(
            order
        )

        return self._to_response(
            order
        )

    async def get_my_orders(
        self,
        user_id: str,
    ) -> list[OrderResponse]:

        orders = await order_repository.get_by_user(
            user_id=user_id
        )

        return [
            self._to_response(order)
            for order in orders
        ]

    async def get_order_by_id(
        self,
        order_id: str,
        user_id: str,
    ) -> OrderResponse:

        order = await order_repository.get_by_id(
            order_id=order_id
        )

        if order is None:
            raise ResourceNotFoundError(
                "Order not found"
            )

        if order.user_id != user_id:
            raise PermissionDeniedError(
                "You are not allowed to access "
                "this order"
            )

        return self._to_response(
            order
        )

    async def update_order_status(
        self,
        order_id: str,
        user_id: str,
        role: str | None,
        new_status: OrderStatus,
    ) -> OrderResponse:

        order = await order_repository.get_by_id(
            order_id=order_id
        )

        if order is None:
            raise ResourceNotFoundError(
                "Order not found"
            )

        allowed_statuses = (
            self._get_allowed_statuses(
                current_status=order.status,
                role=role,
            )
        )

        if new_status not in allowed_statuses:
            raise PermissionDeniedError(
                "You are not allowed to change "
                f"order status from "
                f"'{order.status.value}' to "
                f"'{new_status.value}'"
            )

        order.status = new_status

        order = await order_repository.update(
            order
        )

        return self._to_response(
            order
        )

    def _get_allowed_statuses(
        self,
        current_status: OrderStatus,
        role: str | None,
    ) -> set[OrderStatus]:

        # Customer can only cancel their own
        # pending or confirmed order.
        if role == "customer":

            if current_status in {
                OrderStatus.PENDING,
                OrderStatus.CONFIRMED,
            }:
                return {
                    OrderStatus.CANCELLED
                }

            return set()

        # Restaurant admin controls the
        # food preparation lifecycle.
        if role == "restaurant_admin":

            restaurant_transitions = {
                OrderStatus.PENDING: {
                    OrderStatus.CONFIRMED,
                },
                OrderStatus.CONFIRMED: {
                    OrderStatus.PREPARING,
                },
                OrderStatus.PREPARING: {
                    OrderStatus.READY,
                },
            }

            return restaurant_transitions.get(
                current_status,
                set(),
            )

        # Delivery agent controls delivery
        # lifecycle.
        if role == "delivery_agent":

            delivery_transitions = {
                OrderStatus.READY: {
                    OrderStatus.OUT_FOR_DELIVERY,
                },
                OrderStatus.OUT_FOR_DELIVERY: {
                    OrderStatus.DELIVERED,
                },
            }

            return delivery_transitions.get(
                current_status,
                set(),
            )

        # Admin can perform the complete
        # order lifecycle.
        if role == "admin":

            admin_transitions = {
                OrderStatus.PENDING: {
                    OrderStatus.CONFIRMED,
                    OrderStatus.CANCELLED,
                },
                OrderStatus.CONFIRMED: {
                    OrderStatus.PREPARING,
                    OrderStatus.CANCELLED,
                },
                OrderStatus.PREPARING: {
                    OrderStatus.READY,
                },
                OrderStatus.READY: {
                    OrderStatus.OUT_FOR_DELIVERY,
                },
                OrderStatus.OUT_FOR_DELIVERY: {
                    OrderStatus.DELIVERED,
                },
            }

            return admin_transitions.get(
                current_status,
                set(),
            )

        return set()

    def _calculate_delivery_fee(
        self,
        subtotal: float,
    ) -> float:

        if subtotal >= 500:
            return 0.0

        return 40.0

    def _to_response(
        self,
        order: Order,
    ) -> OrderResponse:

        return OrderResponse(
            id=str(order.id),
            user_id=order.user_id,
            restaurant_id=order.restaurant_id,
            items=[
                {
                    "menu_item_id": item.menu_item_id,
                    "name": item.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price,
                }
                for item in order.items
            ],
            subtotal=order.subtotal,
            delivery_fee=order.delivery_fee,
            total_amount=order.total_amount,
            status=order.status,
            delivery_address=order.delivery_address,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )


order_service = OrderService()

