
from fastapi import APIRouter, Depends

from app.controllers.auth_controller import AuthController
from app.dependencies.auth import get_current_user
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# Controller instance
auth_controller = AuthController()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
async def register(
    request: RegisterRequest,
):
    return await auth_controller.register(request)


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: LoginRequest,
):
    return await auth_controller.login(request)


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
):
    return await auth_controller.get_user_by_id(
        current_user["sub"]
    )

