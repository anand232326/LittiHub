from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    CreateUserProfileRequest,
    UpdateUserProfileRequest,
    UserResponse,
)
from app.services.user_service import UserService


class UserController:

    def __init__(self):
        user_repository = UserRepository()

        self.user_service = UserService(
            user_repository=user_repository
        )

    async def create_profile(
        self,
        auth_user_id: str,
        request: CreateUserProfileRequest,
    ) -> UserResponse:

        return await self.user_service.create_profile(
            auth_user_id=auth_user_id,
            request=request,
        )

    async def get_profile(
        self,
        auth_user_id: str,
    ) -> UserResponse:

        return await self.user_service.get_profile(
            auth_user_id
        )

    async def update_profile(
        self,
        auth_user_id: str,
        request: UpdateUserProfileRequest,
    ) -> UserResponse:

        return await self.user_service.update_profile(
            auth_user_id,
            request,
        )