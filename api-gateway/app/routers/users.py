from typing import Any
from fastapi import APIRouter, Depends, Request, HTTPException, Body
from app.core.exceptions import ResourceNotFoundError
from app.clients.user_client import user_client
from app.core.security import (
    AuthenticatedUser,
    get_current_user,
)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.post("/profile", status_code=201)
async def create_profile(
    request: Request,
    body: dict = Body(...),
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """Proxy endpoint to create a user profile in the user service."""
    return await user_client.create_profile(
        data=body,
        token=request.headers.get("Authorization"),
    )


@router.get("/me")
async def get_my_profile(
    request: Request,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """Proxy endpoint to fetch the currently authenticated user's profile."""
    try:
        return await user_client.get_my_profile(
            token=request.headers.get("Authorization"),
        )
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/me")
async def update_my_profile(
    request: Request,
    body: dict = Body(...),
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """Proxy endpoint to update the currently authenticated user's profile."""
    return await user_client.update_my_profile(
        data=body,
        token=request.headers.get("Authorization"),
    )


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: str,
    request: Request,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """Proxy endpoint to fetch any user by their specific ID."""
    try:
        return await user_client.get_user(
            user_id=user_id,
            token=request.headers.get("Authorization"),
        )
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))