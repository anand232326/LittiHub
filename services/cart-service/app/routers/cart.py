
from fastapi import APIRouter, Depends, status
from app.controllers.cart_controller import cart_controller
from app.dependencies.auth import (
    get_access_token,
    get_current_user,
)
from app.schemas.cart import (
    AddCartItemRequest,
    UpdateCartItemRequest,
    CartResponse,
)


router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"],
)


@router.get(
    "",
    response_model=CartResponse,
)
async def get_cart(
    current_user: dict = Depends(
        get_current_user
    ),
) -> CartResponse:

    return await cart_controller.get_cart(
        user_id=current_user["user_id"],
    )


@router.post(
    "/items",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_item(
    request: AddCartItemRequest,
    current_user: dict = Depends(
        get_current_user
    ),
    access_token: str = Depends(
        get_access_token
    ),
) -> CartResponse:

    return await cart_controller.add_item(
        user_id=current_user["user_id"],
        request=request,
        access_token=access_token,
    )


@router.patch(
    "/items/{menu_item_id}",
    response_model=CartResponse,
)
async def update_item(
    menu_item_id: str,
    request: UpdateCartItemRequest,
    current_user: dict = Depends(
        get_current_user
    ),
    access_token: str = Depends(
        get_access_token
    ),
) -> CartResponse:

    return await cart_controller.update_item(
        user_id=current_user["user_id"],
        menu_item_id=menu_item_id,
        request=request,
        access_token=access_token,
    )


@router.delete(
    "/items/{menu_item_id}",
    response_model=CartResponse,
)
async def remove_item(
    menu_item_id: str,
    current_user: dict = Depends(
        get_current_user
    ),
) -> CartResponse:

    return await cart_controller.remove_item(
        user_id=current_user["user_id"],
        menu_item_id=menu_item_id,
    )


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_cart(
    current_user: dict = Depends(
        get_current_user
    ),
) -> None:

    await cart_controller.clear_cart(
        user_id=current_user["user_id"],
    )
