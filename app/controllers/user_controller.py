from fastapi import HTTPException, status

from app.services.user_service import user_service
from app.schemas.auth import UserResponse


class UserController:

    async def get_by_id(
        self,
        user_id: str,
    ) -> UserResponse:

        user = await user_service.get_by_id(
            user_id
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user


user_controller = UserController()