from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user, require_role
from app.core.enums import UserRole
from app.models.user import User
from app.schemas.auth import UserResponse,UserUpdate
from app.controllers.user_controller import user_controller

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# ✅ 1. Static routes go FIRST
@router.get("/admin-test")
async def admin_test(
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
):
    return {
        "message": "Admin access granted",
        "user_id": str(current_user.id),
        "role": current_user.role,
    }


# ✅ 2. Dynamic path parameters go LAST
@router.get("/{user_id}")
async def get_user(
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    return await user_controller.get_by_id(
        user_id
    )


@router.patch("/me",response_model=UserResponse,)
async def update_my_profile(user_data: UserUpdate,current_user: User = Depends(get_current_user),):
    return await user_controller.update_me(
        user_data=user_data,
        current_user=current_user,
    )