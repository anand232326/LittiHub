from fastapi import APIRouter, status,Depends
from app.core.exceptions import UserAlreadyExistsError
from app.controllers.auth_controller import auth_controller
from app.schemas.auth import UserCreate, UserResponse,LoginResponse,LoginRequest
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=UserResponse,status_code=status.HTTP_201_CREATED,)
async def register(user_data: UserCreate):
    return await auth_controller.register(user_data)

@router.post("/login",response_model=LoginResponse)
async def login(login_data:LoginRequest):
    return await auth_controller.login(login_data)


@router.get("/me")
async def get_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
    }
