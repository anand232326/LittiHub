from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    Header,
    Request,
)

from app.clients.order_client import order_client
from app.core.security import (
    AuthenticatedUser,
    get_current_user,
)


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"],
)


@router.post("")
async def create_order(
    data: dict[str, Any],
    request: Request,
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key",
    ),
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await order_client.create_order(
        data=data,
        token=request.headers["Authorization"],
        idempotency_key=idempotency_key,
    )


@router.get("")
async def get_orders(
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await order_client.get_orders(
        token=request.headers["Authorization"],
    )


@router.get("/{order_id}")
async def get_order(
    order_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await order_client.get_order(
        order_id=order_id,
        token=request.headers["Authorization"],
    )


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: str,
    data: dict[str, Any],
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await order_client.update_order_status(
        order_id=order_id,
        data=data,
        token=request.headers["Authorization"],
    )