
from app.clients.menu_client import menu_client
from app.core.exceptions import (
    InvalidRequestError,
    ResourceNotFoundError,
)
from app.models.cart import Cart, CartItem
from app.repositories.cart_repository import CartRepository
from app.schemas.cart import (
    AddCartItemRequest,
    UpdateCartItemRequest,
    CartResponse,
)


class CartService:

    def __init__(
        self,
        repository: CartRepository,
    ):
        self.repository = repository

    async def get_cart(
        self,
        user_id: str,
    ) -> CartResponse:

        cart = await self.repository.get_cart(
            user_id
        )

        if not cart:
            cart = Cart(
                user_id=user_id
            )

        return self._to_response(cart)

    async def add_item(
        self,
        user_id: str,
        request: AddCartItemRequest,
    ) -> CartResponse:

        menu_item = await menu_client.get_menu_item(
            restaurant_id=request.restaurant_id,
            item_id=request.menu_item_id,
        )

        if not menu_item.get("is_active"):
            raise ResourceNotFoundError(
                "Menu item is not active"
            )

        if not menu_item.get("is_available"):
            raise ResourceNotFoundError(
                "Menu item is currently unavailable"
            )

        cart = await self.repository.get_cart(
            user_id
        )

        if not cart:

            cart = Cart(
                user_id=user_id,
                restaurant_id=request.restaurant_id,
            )

        if cart.restaurant_id is None:

            cart.restaurant_id = (
                request.restaurant_id
            )

        elif cart.restaurant_id != request.restaurant_id:

            raise InvalidRequestError(
                "Cart can contain items from only "
                "one restaurant"
            )

        existing_item = next(
            (
                item
                for item in cart.items
                if item.menu_item_id
                == request.menu_item_id
            ),
            None,
        )

        price = float(
            menu_item["price"]
        )

        name = menu_item["name"]

        if existing_item:

            new_quantity = (
                existing_item.quantity
                + request.quantity
            )

            if new_quantity > 20:

                raise InvalidRequestError(
                    "Maximum quantity for a menu item "
                    "is 20"
                )

            existing_item.quantity = (
                new_quantity
            )

            existing_item.price = price

            existing_item.name = name

            existing_item.total_price = (
                price * new_quantity
            )

        else:

            total_price = (
                price * request.quantity
            )

            cart.items.append(
                CartItem(
                    menu_item_id=request.menu_item_id,
                    name=name,
                    price=price,
                    quantity=request.quantity,
                    total_price=total_price,
                )
            )

        self._recalculate(cart)

        cart = await self.repository.save_cart(
            cart
        )

        return self._to_response(cart)

    async def update_item(
        self,
        user_id: str,
        menu_item_id: str,
        request: UpdateCartItemRequest,
    ) -> CartResponse:

        cart = await self.repository.get_cart(
            user_id
        )

        if not cart:

            raise ResourceNotFoundError(
                "Cart not found"
            )

        item = next(
            (
                item
                for item in cart.items
                if item.menu_item_id
                == menu_item_id
            ),
            None,
        )

        if not item:

            raise ResourceNotFoundError(
                "Menu item not found in cart"
            )

        menu_item = await menu_client.get_menu_item(
            restaurant_id=cart.restaurant_id,
            item_id=menu_item_id,
        )

        if not menu_item.get("is_active"):

            raise ResourceNotFoundError(
                "Menu item is not active"
            )

        if not menu_item.get("is_available"):

            raise ResourceNotFoundError(
                "Menu item is currently unavailable"
            )

        item.quantity = request.quantity

        item.price = float(
            menu_item["price"]
        )

        item.name = menu_item["name"]

        item.total_price = (
            item.price * item.quantity
        )

        self._recalculate(cart)

        cart = await self.repository.save_cart(
            cart
        )

        return self._to_response(cart)

    async def remove_item(
        self,
        user_id: str,
        menu_item_id: str,
    ) -> CartResponse:

        cart = await self.repository.get_cart(
            user_id
        )

        if not cart:

            raise ResourceNotFoundError(
                "Cart not found"
            )

        original_length = len(
            cart.items
        )

        cart.items = [
            item
            for item in cart.items
            if item.menu_item_id
            != menu_item_id
        ]

        if len(cart.items) == original_length:

            raise ResourceNotFoundError(
                "Menu item not found in cart"
            )

        if not cart.items:

            await self.repository.delete_cart(
                user_id
            )

            return self._to_response(
                Cart(user_id=user_id)
            )

        self._recalculate(cart)

        cart = await self.repository.save_cart(
            cart
        )

        return self._to_response(cart)

    async def clear_cart(
        self,
        user_id: str,
    ) -> None:

        await self.repository.delete_cart(
            user_id
        )

    @staticmethod
    def _recalculate(
        cart: Cart,
    ) -> None:

        cart.subtotal = sum(
            item.total_price
            for item in cart.items
        )

        cart.total_items = sum(
            item.quantity
            for item in cart.items
        )

    @staticmethod
    def _to_response(
        cart: Cart,
    ) -> CartResponse:

        return CartResponse(
            user_id=cart.user_id,
            restaurant_id=cart.restaurant_id,
            items=cart.items,
            subtotal=cart.subtotal,
            total_items=cart.total_items,
        )


cart_service = CartService(
    repository=CartRepository()
)

