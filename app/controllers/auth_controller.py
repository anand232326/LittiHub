from fastapi import HTTPException, status

from app.core.exceptions import UserAlreadyExistsError,InvalidCredentialsError
from app.schemas.auth import UserCreate, UserResponse,LoginResponse,LoginRequest
from app.services.auth_service import auth_service


class AuthController:

    async def register(self,user_data: UserCreate,) -> UserResponse:
        try:
            user = await auth_service.register(
                email=user_data.email,
                full_name=user_data.full_name,
                phone=user_data.phone,
                password=user_data.password,
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

        except UserAlreadyExistsError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            )


    async def login(self,login_data:LoginRequest):
        try:
            access_token=await auth_service.login(login_data)
            return LoginResponse(
                access_token=access_token,
                token_type="bearer"
            )
        except InvalidCredentialsError as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(error)
            )


auth_controller = AuthController()