
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
            user_id=user_id
        )

        if cart is None:
            cart = Cart(
                user_id=user_id
            )

        return self._to_response(cart)



    async def add_item(
        self,
        user_id: str,
        request: AddCartItemRequest,
        access_token: str,
    ) -> CartResponse:

        async with self.repository.get_cart_lock(
            user_id
        ):

            menu_item = await menu_client.get_menu_item(
                restaurant_id=request.restaurant_id,
                item_id=request.menu_item_id,
                access_token=access_token,
            )

            self._validate_menu_item(
                menu_item
            )

            cart = await self.repository.get_cart(
                user_id=user_id
            )

            if cart is None:
                cart = Cart(
                    user_id=user_id,
                    restaurant_id=request.restaurant_id,
                )

            self._validate_restaurant(
                cart=cart,
                restaurant_id=request.restaurant_id,
            )

            existing_item = self._find_item(
                cart=cart,
                menu_item_id=request.menu_item_id,
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
                        "Maximum quantity for a menu item is 20"
                    )

                existing_item.quantity = new_quantity
                existing_item.name = name
                existing_item.price = price
                existing_item.total_price = (
                    price * new_quantity
                )

            else:

                cart.items.append(
                    CartItem(
                        menu_item_id=request.menu_item_id,
                        name=name,
                        price=price,
                        quantity=request.quantity,
                        total_price=(
                            price * request.quantity
                        ),
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
        access_token: str,
    ) -> CartResponse:

        async with self.repository.get_cart_lock(
            user_id
        ):

            cart = await self.repository.get_cart(
                user_id=user_id
            )

            if cart is None:
                raise ResourceNotFoundError(
                    "Cart not found"
                )

            if cart.restaurant_id is None:
                raise InvalidRequestError(
                    "Cart does not have a restaurant"
                )

            item = self._find_item(
                cart=cart,
                menu_item_id=menu_item_id,
            )

            if item is None:
                raise ResourceNotFoundError(
                    "Menu item not found in cart"
                )

            menu_item = await menu_client.get_menu_item(
                restaurant_id=cart.restaurant_id,
                item_id=menu_item_id,
                access_token=access_token,
            )

            self._validate_menu_item(
                menu_item
            )

            price = float(
                menu_item["price"]
            )

            item.quantity = request.quantity
            item.name = menu_item["name"]
            item.price = price
            item.total_price = (
                price * request.quantity
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

        async with self.repository.get_cart_lock(
            user_id
        ):

            cart = await self.repository.get_cart(
                user_id=user_id
            )

            if cart is None:
                raise ResourceNotFoundError(
                    "Cart not found"
                )

            item = self._find_item(
                cart=cart,
                menu_item_id=menu_item_id,
            )

            if item is None:
                raise ResourceNotFoundError(
                    "Menu item not found in cart"
                )

            cart.items = [
                cart_item
                for cart_item in cart.items
                if cart_item.menu_item_id != menu_item_id
            ]

            if not cart.items:

                await self.repository.delete_cart(
                    user_id=user_id
                )

                return self._to_response(
                    Cart(
                        user_id=user_id
                    )
                )

            self._recalculate(cart)

            cart = await self.repository.save_cart(
                cart
            )

            return self._to_response(cart)



    async def get_cart_for_checkout(
    self,
    user_id: str,
    ) -> CartResponse:

        cart = await self.repository.get_cart(
        user_id=user_id
        )

        if cart is None:
            raise ResourceNotFoundError(
            "Cart not found"
        )

        if not cart.items:
            raise InvalidRequestError(
            "Cart is empty"
        )

        return self._to_response(cart)

    


    async def clear_cart(
        self,
        user_id: str,
    ) -> None:

        async with self.repository.get_cart_lock(
            user_id
        ):

            await self.repository.delete_cart(
                user_id=user_id
            )




    @staticmethod
    def _validate_menu_item(
        menu_item: dict,
    ) -> None:

        if not menu_item.get("is_active"):
            raise ResourceNotFoundError(
                "Menu item is not active"
            )

        if not menu_item.get("is_available"):
            raise ResourceNotFoundError(
                "Menu item is currently unavailable"
            )

    @staticmethod
    def _validate_restaurant(
        cart: Cart,
        restaurant_id: str,
    ) -> None:

        if cart.restaurant_id is None:
            cart.restaurant_id = restaurant_id
            return

        if cart.restaurant_id != restaurant_id:
            raise InvalidRequestError(
                "Cart can contain items from only one restaurant"
            )

    @staticmethod
    def _find_item(
        cart: Cart,
        menu_item_id: str,
    ) -> CartItem | None:

        return next(
            (
                item
                for item in cart.items
                if item.menu_item_id == menu_item_id
            ),
            None,
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

