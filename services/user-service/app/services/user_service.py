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

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_profile(
        self,
        auth_user_id: str,
        request: CreateUserProfileRequest,
    ) -> UserResponse:

        existing_user = await self.user_repository.get_by_auth_user_id(
            auth_user_id
        )

        if existing_user:
            raise ResourceAlreadyExistsError(
                "User profile already exists"
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

        user = await self.user_repository.get_by_auth_user_id(
            auth_user_id
        )

        if not user:
            raise ResourceNotFoundError(
                "User profile not found"
            )

        return self._to_response(user)

    async def update_profile(
        self,
        auth_user_id: str,
        request: UpdateUserProfileRequest,
    ) -> UserResponse:

        user = await self.user_repository.get_by_auth_user_id(
            auth_user_id
        )

        if not user:
            raise ResourceNotFoundError(
                "User profile not found"
            )

        update_data = request.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        return self._to_response(
            await self.user_repository.update(user)
        )

    @staticmethod
    def _to_response(user: User) -> UserResponse:

        return UserResponse(
            id=str(user.id),
            auth_user_id=user.auth_user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )