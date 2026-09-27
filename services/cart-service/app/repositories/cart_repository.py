
import json

from app.core.database import redis_client
from app.models.cart import Cart


class CartRepository:

    CART_KEY_PREFIX = "cart:"

    def _get_key(
        self,
        user_id: str,
    ) -> str:

        return (
            f"{self.CART_KEY_PREFIX}"
            f"{user_id}"
        )

    async def get_cart(
        self,
        user_id: str,
    ) -> Cart | None:

        key = self._get_key(
            user_id
        )

        data = await redis_client.get(
            key
        )

        if data is None:
            return None

        return Cart.model_validate_json(
            data
        )

    async def save_cart(
        self,
        cart: Cart,
    ) -> Cart:

        key = self._get_key(
            cart.user_id
        )

        await redis_client.set(
            key,
            cart.model_dump_json(),
        )

        return cart

    async def delete_cart(
        self,
        user_id: str,
    ) -> None:

        key = self._get_key(
            user_id
        )

        await redis_client.delete(
            key
        )


cart_repository = CartRepository()

