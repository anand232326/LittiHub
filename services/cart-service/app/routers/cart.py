
from fastapi import APIRouter, Depends, status
from app.controllers.cart_controller import cart_controller
from app.dependencies.auth import get_current_user
from app.models.cart import Cart
from app.schemas.cart import (
    AddCartItemRequest,
    UpdateCartItemRequest,
    CartResponse,
)


router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"],
)



@router.get("",response_model=CartResponse,status_code=status.HTTP_200_OK,)
async def get_cart(current_user: Cart = Depends(get_current_user),):
    return await cart_controller.get_cart(
        user_id=str(current_user.id)
    )


@router.post(
    "/items",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_item(
    request: AddCartItemRequest,
    current_user: Cart = Depends(
        get_current_user
    ),
):
    return await cart_controller.add_item(
        user_id=str(current_user.id),
        request=request,
    )


@router.patch(
    "/items/{menu_item_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def update_item(
    menu_item_id: str,
    request: UpdateCartItemRequest,
    current_user: Cart = Depends(
        get_current_user
    ),
):
    return await cart_controller.update_item(
        user_id=str(current_user.id),
        menu_item_id=menu_item_id,
        request=request,
    )


@router.delete(
    "/items/{menu_item_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def remove_item(
    menu_item_id: str,
    current_user: Cart = Depends(
        get_current_user
    ),
):
    return await cart_controller.remove_item(
        user_id=str(current_user.id),
        menu_item_id=menu_item_id,
    )


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_cart(
    current_user: Cart = Depends(
        get_current_user
    ),
):
    await cart_controller.clear_cart(
        user_id=str(current_user.id)
    )

