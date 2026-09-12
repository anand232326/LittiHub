
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)
from app.services.auth_service import AuthService


class AuthController:
    """
    Handles authentication use cases at the API/controller layer.
    """

    def __init__(self):
        user_repository = UserRepository()
        self.auth_service = AuthService(
            user_repository=user_repository
        )

    async def register(
        self,
        request: RegisterRequest,
    ) -> UserResponse:
        return await self.auth_service.register(request)

    async def login(
        self,
        request: LoginRequest,
    ) -> LoginResponse:
        return await self.auth_service.login(request)

    async def get_user_by_id(
        self,
        user_id: str,
    ) -> UserResponse:
        return await self.auth_service.get_user_by_id(user_id)
