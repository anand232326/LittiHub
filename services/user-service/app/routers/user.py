from fastapi import APIRouter, Depends

from app.controllers.user_controller import UserController
from app.dependencies.auth import get_current_user
from app.schemas.user import (
    CreateUserProfileRequest,
    UpdateUserProfileRequest,
    UserResponse,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

user_controller = UserController()


@router.post(
    "/profile",
    response_model=UserResponse,
    status_code=201,
)
async def create_profile(
    request: CreateUserProfileRequest,
    current_user: dict = Depends(get_current_user),
):

    auth_user_id = current_user["sub"]

    return await user_controller.create_profile(
        auth_user_id=auth_user_id,
        request=request,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
):

    auth_user_id = current_user["sub"]

    return await user_controller.get_profile(
        auth_user_id
    )


@router.patch(
    "/me",
    response_model=UserResponse,
)
async def update_my_profile(
    request: UpdateUserProfileRequest,
    current_user: dict = Depends(get_current_user),
):

    auth_user_id = current_user["sub"]

    return await user_controller.update_profile(
        auth_user_id=auth_user_id,
        request=request,
    )