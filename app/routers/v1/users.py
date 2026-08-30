from fastapi import APIRouter, Depends

from app.controllers.user_controller import user_controller
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    return await user_controller.get_by_id(
        user_id
    )