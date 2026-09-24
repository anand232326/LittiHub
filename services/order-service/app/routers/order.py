
from fastapi import APIRouter, Depends, status

from app.controllers.order_controller import (
    order_controller,
)
from app.dependencies.auth import (
    get_current_user,
)
from app.schemas.order import (
    CreateOrderRequest,
    OrderResponse,
    UpdateOrderStatusRequest,
)


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"],
)


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    request: CreateOrderRequest,
    current_user: dict = Depends(
        get_current_user
    ),
) -> OrderResponse:

    return await order_controller.create_order(
        user_id=current_user["user_id"],
        request=request,
    )


@router.get(
    "",
    response_model=list[OrderResponse],
)
async def get_my_orders(
    current_user: dict = Depends(
        get_current_user
    ),
) -> list[OrderResponse]:

    return await order_controller.get_my_orders(
        user_id=current_user["user_id"],
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
async def get_order_by_id(
    order_id: str,
    current_user: dict = Depends(
        get_current_user
    ),
) -> OrderResponse:

    return await order_controller.get_order_by_id(
        order_id=order_id,
        user_id=current_user["user_id"],
    )


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
async def update_order_status(
    order_id: str,
    request: UpdateOrderStatusRequest,
    current_user: dict = Depends(
        get_current_user
    ),
) -> OrderResponse:

    return await order_controller.update_order_status(
        order_id=order_id,
        user_id=current_user["user_id"],
        role=current_user.get("role"),
        new_status=request.status,
    )
