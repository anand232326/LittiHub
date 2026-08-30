from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserResponse
from app.services.redis_service import redis_service
from app.schemas.auth import UserUpdate
from app.models.user import User
from datetime import datetime, timezone

class UserService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.redis_service = redis_service

    async def get_by_id(
        self,
        user_id: str,
    ) -> UserResponse | None:

        cache_key = f"user:{user_id}"

        # 1. Check Redis
        cached_user = await self.redis_service.get_json(
            cache_key
        )

        if cached_user is not None:
            return UserResponse(**cached_user)

        # 2. Cache miss → MongoDB
        user = await self.user_repository.get_by_id(
            user_id
        )

        if user is None:
            return None

        # 3. Convert database model → DTO
        user_response = UserResponse(
            id=str(user.id),
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            role=user.role,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        # 4. Store DTO in Redis
        await self.redis_service.set_json(
            key=cache_key,
            value=user_response.model_dump(mode="json"),
            expire=300,
        )

        # 5. Return DTO
        return user_response



    async def update_me(self,user: User,user_data: UserUpdate,) -> UserResponse:
        if user_data.full_name is not None:
            user.full_name = user_data.full_name
 

        if user_data.phone is not None:
            user.phone = user_data.phone

        user.updated_at = datetime.now(timezone.utc)

        user = await self.user_repository.update(user)

        await self.redis_service.delete(
            f"user:{user.id}"
        )

        return UserResponse(
            id=str(user.id),
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            role=user.role,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


user_service = UserService()