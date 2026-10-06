from typing import Any

from fastapi import APIRouter, Depends, Request

from app.clients.auth_client import auth_client
from app.core.security import (
    AuthenticatedUser,
    get_current_user,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post("/register")
async def register(
    data: dict[str, Any],
):
    return await auth_client.register(
        data=data,
    )


@router.post("/login")
async def login(
    data: dict[str, Any],
):
    return await auth_client.login(
        data=data,
    )


@router.get("/me")
async def get_current_user_profile(
    request: Request,
    current_user: AuthenticatedUser = Depends(
        get_current_user
    ),
):
    return await auth_client.get_me(
        token=request.headers["Authorization"],
    )