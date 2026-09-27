
from app.schemas.cart import (
    AddCartItemRequest,
    UpdateCartItemRequest,
    CartResponse,
)
from app.services.cart_service import cart_service


class CartController:

    async def get_cart(self,user_id: str,) -> CartResponse:
        return await cart_service.get_cart(
            user_id=user_id
        )



    async def add_item(self,user_id: str,request: AddCartItemRequest,) -> CartResponse:
        return await cart_service.add_item(
            user_id=user_id,
            request=request,
        )


    async def update_item(self,user_id: str,menu_item_id: str,request: UpdateCartItemRequest,) -> CartResponse:
        return await cart_service.update_item(
            user_id=user_id,
            menu_item_id=menu_item_id,
            request=request,
        )



    async def remove_item(self,user_id: str,menu_item_id: str,) -> CartResponse:
        return await cart_service.remove_item(
            user_id=user_id,
            menu_item_id=menu_item_id,
        )



    async def clear_cart(self,user_id: str,) -> None:
        await cart_service.clear_cart(
            user_id=user_id
        )


cart_controller = CartController()
