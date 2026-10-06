from fastapi import APIRouter, Depends, Request

from app.clients.user_client import user_client
from app.core.security import (
    AuthenticatedUser,
    get_current_user,
)


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await user_client.get_user(
        user_id=user_id,
        token=request.headers["Authorization"],
    )