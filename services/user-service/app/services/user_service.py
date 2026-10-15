
from app.core.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    CreateUserProfileRequest,
    UpdateUserProfileRequest,
    UserResponse,
)


class UserService:
    """Business logic for user profile operations."""

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    async def create_profile(
        self,
        auth_user_id: str,
        request: CreateUserProfileRequest,
    ) -> UserResponse:
        """Create a profile for an authenticated user."""

        existing_user = (
            await self.user_repository.get_by_auth_user_id(
                auth_user_id
            )
        )

        if existing_user is not None:
            raise ResourceAlreadyExistsError(
                "User profile already exists."
            )

        user = User(
            auth_user_id=auth_user_id,
            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone,
        )

        created_user = await self.user_repository.create(user)

        return self._to_response(created_user)

    async def get_profile(
        self,
        auth_user_id: str,
    ) -> UserResponse:
        """Retrieve a user's profile using their authentication ID."""

        user = await self.user_repository.get_by_auth_user_id(
            auth_user_id
        )

        if user is None:
            raise ResourceNotFoundError(
                "User profile not found."
            )

        return self._to_response(user)

    async def get_user_by_id(
        self,
        user_id: str,
    ) -> User:
        """Retrieve a user using their database ID."""

        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise ResourceNotFoundError(
                f"User with ID '{user_id}' not found."
            )

        return user

    async def update_profile(
        self,
        auth_user_id: str,
        request: UpdateUserProfileRequest,
    ) -> UserResponse:
        """Update an authenticated user's profile."""

        user = await self.user_repository.get_by_auth_user_id(
            auth_user_id
        )

        if user is None:
            raise ResourceNotFoundError(
                "User profile not found."
            )

        update_data = request.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        updated_user = await self.user_repository.update(user)

        return self._to_response(updated_user)

    @staticmethod
    def _to_response(user: User) -> UserResponse:
        """Convert a database model into a public response schema."""

        return UserResponse(
            id=str(user.id),
            auth_user_id=user.auth_user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
