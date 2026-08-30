from fastapi import HTTPException, status,Depends
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import UserUpdate
from app.services.user_service import user_service
from app.schemas.auth import UserResponse


class UserController:

    async def get_by_id(self,user_id: str,) -> UserResponse:
        user = await user_service.get_by_id(
            user_id
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user


    async def update_me(self,user_data: UserUpdate,current_user: User = Depends(get_current_user),) -> UserResponse:

        return await user_service.update_me(
        user=current_user,
        user_data=user_data,
      )

user_controller = UserController()