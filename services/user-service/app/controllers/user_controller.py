from fastapi import HTTPException, status
from app.core.exceptions import ResourceNotFoundError
from app.schemas.user import (
    CreateUserProfileRequest,
    UpdateUserProfileRequest,
    UserResponse,
)
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


class UserController:
    """Handle user profile requests and coordinate service operations."""

    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.user_service = UserService(
            user_repository=self.user_repository
        )

    async def create_profile(
        self,
        auth_user_id: str,
        request: CreateUserProfileRequest,
    ) -> UserResponse:
        """Create a profile for the authenticated user."""
        return await self.user_service.create_profile(
            auth_user_id=auth_user_id,
            request=request,
        )

    async def get_profile(
        self,
        auth_user_id: str,
    ) -> dict:
        """Fetch the profile of the authenticated user."""
        if not auth_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication",
            )

        user = await self.user_service.get_profile(
            auth_user_id=auth_user_id,
        )

        user_dict = user.model_dump(by_alias=True)
        user_dict["id"] = str(user.id)

        return user_dict

    async def update_profile(
        self,
        auth_user_id: str,
        request: UpdateUserProfileRequest,
    ) -> UserResponse:
        """Update the authenticated user's profile."""
        return await self.user_service.update_profile(
            auth_user_id=auth_user_id,
            request=request,
        )

    async def get_user_by_id(
        self,
        user_id: str,
    ) -> dict:
        """Fetch a user profile by its ID."""
        try:
            user = await self.user_service.get_user_by_id(
                user_id=user_id,
            )

            user_dict = user.model_dump(by_alias=True)
            user_dict["id"] = str(user.id)

            return user_dict

        except ResourceNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

