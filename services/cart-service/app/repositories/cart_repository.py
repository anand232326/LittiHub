
import json
from redis.asyncio import Redis
from app.core.config import Config
from app.core.database import redis_client
from app.models.cart import Cart


class CartRepository:

    CART_KEY_PREFIX = "cart:"
    LOCK_KEY_PREFIX = "lock:cart:"

    def _get_key( self,user_id: str,) -> str:
        return (
            f"{self.CART_KEY_PREFIX}"
            f"{user_id}"
        )


    def _get_lock_key( self, user_id: str, ) -> str: 
        return f"{self.LOCK_KEY_PREFIX}{user_id}"


    
    async def get_cart(self,user_id: str,) -> Cart | None:
        key = self._get_key(user_id)
        data = await redis_client.get(key)
        if data is None:
            return None

        return Cart.model_validate_json(
            data
        )




    async def save_cart(self,cart: Cart,) -> Cart:
        key = self._get_key(
            cart.user_id
        )

        await redis_client.set(
            key,
            cart.model_dump_json(),
            ex=Config.CART_TTL_SECONDS,
        )
        return cart


    async def delete_cart(self,user_id: str,) -> None:
        key = self._get_key(
            user_id
        )

        await redis_client.delete(
            key
        )



    def get_cart_lock( self, user_id: str, ): 
        lock_key = self._get_lock_key( user_id ) 
        return redis_client.lock( 
            lock_key, timeout=10, blocking_timeout=5, )

    

cart_repository = CartRepository()

