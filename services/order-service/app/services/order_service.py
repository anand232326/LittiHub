
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone
from app.clients.cart_client import cart_client
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

from app.utils.idempotency import (
    generate_idempotency_hash,
)


class OrderService:

    # =========================================================
    # CREATE ORDER
    # =========================================================

    async def create_order(
        self,
        user_id: str,
        request: CreateOrderRequest,
        access_token: str,
        idempotency_key: str,
    ) -> OrderResponse:

        # -----------------------------------------------------
        # 1. Get cart
        # -----------------------------------------------------

        cart = await cart_client.get_cart(
            user_id=user_id,
            access_token=access_token,
        )

        if not cart.get("items"):
            raise InvalidRequestError(
                "Cannot create an order from an empty cart"
            )

        restaurant_id = cart.get(
            "restaurant_id"
        )

        if not restaurant_id:
            raise InvalidRequestError(
                "Cart is not associated with a restaurant"
            )

        # -----------------------------------------------------
        # 2. Validate restaurant from request
        # -----------------------------------------------------

        if request.restaurant_id != restaurant_id:
            raise InvalidRequestError(
                "Restaurant does not match the cart"
            )

        # -----------------------------------------------------
        # 3. Generate idempotency request hash
        # -----------------------------------------------------

        idempotency_request_hash = (
            generate_idempotency_hash(
                restaurant_id=restaurant_id,
                delivery_address=request.delivery_address,
                cart_items=cart["items"],
            )
        )

        # -----------------------------------------------------
        # 4. Check existing order
        # -----------------------------------------------------

        existing_order = (
            await order_repository.find_by_idempotency_key(
                user_id=user_id,
                idempotency_key=idempotency_key,
            )
        )

        if existing_order is not None:

            if (
                existing_order.idempotency_request_hash
                != idempotency_request_hash
            ):
                raise InvalidRequestError(
                    "Idempotency key was already used "
                    "for a different checkout request"
                )

            return self._to_response(
                existing_order
            )

        # -----------------------------------------------------
        # 5. Validate user
        # -----------------------------------------------------

        user = await user_client.get_user(
            user_id=user_id,
        )

        if user is None:
            raise ResourceNotFoundError(
                "User not found"
            )

        # -----------------------------------------------------
        # 6. Validate restaurant
        # -----------------------------------------------------

        restaurant = await restaurant_client.get_restaurant(
            restaurant_id=restaurant_id,
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

        # -----------------------------------------------------
        # 7. Validate cart items with Menu Service
        # -----------------------------------------------------

        order_items: list[OrderItem] = []
        subtotal = 0.0

        for cart_item in cart["items"]:

            menu_item = await menu_client.get_menu_item(
                restaurant_id=restaurant_id,
                item_id=cart_item["menu_item_id"],
                access_token=access_token,
            )

            if menu_item is None:
                raise ResourceNotFoundError(
                    f"Menu item "
                    f"'{cart_item['menu_item_id']}' "
                    f"not found"
                )

            # -------------------------------------------------
            # Verify restaurant ownership
            # -------------------------------------------------

            if (
                menu_item.get("restaurant_id")
                != restaurant_id
            ):
                raise InvalidRequestError(
                    "Menu item does not belong "
                    "to this restaurant"
                )

            # -------------------------------------------------
            # Verify active status
            # -------------------------------------------------

            if not menu_item.get(
                "is_active",
                False,
            ):
                raise InvalidRequestError(
                    f"Menu item "
                    f"'{menu_item.get('name')}' "
                    f"is inactive"
                )

            # -------------------------------------------------
            # Verify availability
            # -------------------------------------------------

            if not menu_item.get(
                "is_available",
                False,
            ):
                raise InvalidRequestError(
                    f"Menu item "
                    f"'{menu_item.get('name')}' "
                    f"is currently unavailable"
                )

            # -------------------------------------------------
            # Use current Menu Service price
            # -------------------------------------------------

            unit_price = float(
                menu_item["price"]
            )

            quantity = cart_item["quantity"]

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

        # -----------------------------------------------------
        # 8. Calculate delivery fee
        # -----------------------------------------------------

        delivery_fee = (
            self._calculate_delivery_fee(
                subtotal=subtotal
            )
        )

        # -----------------------------------------------------
        # 9. Calculate total amount
        # -----------------------------------------------------

        total_amount = (
            subtotal + delivery_fee
        )

        # -----------------------------------------------------
        # 10. Create Order document
        # -----------------------------------------------------

        order = Order(
            user_id=user_id,
            restaurant_id=restaurant_id,
            idempotency_key=idempotency_key,
            idempotency_request_hash=(
                idempotency_request_hash
            ),
            items=order_items,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
            delivery_address=request.delivery_address,
        )

        # -----------------------------------------------------
        # 11. Save order
        # -----------------------------------------------------

        try:

            order = await order_repository.create(
                order
            )

        except DuplicateKeyError:

            # Another request with the same
            # idempotency key created the order first.

            existing_order = (
                await order_repository.find_by_idempotency_key(
                    user_id=user_id,
                    idempotency_key=idempotency_key,
                )
            )

            if existing_order is None:
                raise

            if (
                existing_order.idempotency_request_hash
                != idempotency_request_hash
            ):
                raise InvalidRequestError(
                    "Idempotency key was already used "
                    "for a different checkout request"
                )

            return self._to_response(
                existing_order
            )

        # -----------------------------------------------------
        # 12. Clear cart after successful order creation
        # -----------------------------------------------------

        await cart_client.clear_cart(
            user_id=user_id,
            access_token=access_token,
        )

        # -----------------------------------------------------
        # 13. Return created order
        # -----------------------------------------------------

        return self._to_response(
            order
        )

    # =========================================================
    # GET MY ORDERS
    # =========================================================

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

    # =========================================================
    # GET ORDER BY ID
    # =========================================================

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
                "You are not allowed to access this order"
            )

        return self._to_response(
            order
        )

    # =========================================================
    # UPDATE ORDER STATUS
    # =========================================================

    async def update_order_status(
        self,
        order_id: str,
        user_id: str,
        role: str,
        new_status: OrderStatus,
    ) -> OrderResponse:

        order = await order_repository.get_by_id(
            order_id=order_id
        )

        if order is None:
            raise ResourceNotFoundError(
                "Order not found"
            )

        # -----------------------------------------------------
        # Customer can only update their own order
        # -----------------------------------------------------

        if (
            role == "customer"
            and order.user_id != user_id
        ):
            raise PermissionDeniedError(
                "You are not allowed to update this order"
            )

        # -----------------------------------------------------
        # Prevent invalid status transitions
        # -----------------------------------------------------

        self._validate_status_transition(
            current_status=order.status,
            new_status=new_status,
        )

        order.status = new_status

        order.updated_at = (
            datetime.now(timezone.utc)
        )

        order = await order_repository.update(
            order
        )

        return self._to_response(
            order
        )

    # =========================================================
    # DELIVERY FEE
    # =========================================================

    @staticmethod
    def _calculate_delivery_fee(
        subtotal: float,
    ) -> float:

        if subtotal >= 500:
            return 0.0

        return 40.0

    # =========================================================
    # STATUS TRANSITION VALIDATION
    # =========================================================

    @staticmethod
    def _validate_status_transition(
        current_status: OrderStatus,
        new_status: OrderStatus,
    ) -> None:

        allowed_transitions = {

            OrderStatus.PENDING: {
                OrderStatus.CONFIRMED,
                OrderStatus.CANCELLED,
            },

            OrderStatus.CONFIRMED: {
                OrderStatus.PREPARING,
                OrderStatus.CANCELLED,
            },

            OrderStatus.PREPARING: {
                OrderStatus.READY_FOR_PICKUP,
            },

            OrderStatus.READY_FOR_PICKUP: {
                OrderStatus.OUT_FOR_DELIVERY,
            },

            OrderStatus.OUT_FOR_DELIVERY: {
                OrderStatus.DELIVERED,
            },

            OrderStatus.DELIVERED: set(),

            OrderStatus.CANCELLED: set(),
        }

        allowed = allowed_transitions.get(
            current_status,
            set(),
        )

        if new_status not in allowed:
            raise InvalidRequestError(
                f"Invalid order status transition: "
                f"{current_status} -> {new_status}"
            )

    # =========================================================
    # RESPONSE
    # =========================================================

    @staticmethod
    def _to_response(
        order: Order,
    ) -> OrderResponse:

        return OrderResponse(
            id=str(order.id),
            user_id=order.user_id,
            restaurant_id=order.restaurant_id,
            items=order.items,
            subtotal=order.subtotal,
            delivery_fee=order.delivery_fee,
            total_amount=order.total_amount,
            status=order.status,
            delivery_address=order.delivery_address,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )


order_service = OrderService()
