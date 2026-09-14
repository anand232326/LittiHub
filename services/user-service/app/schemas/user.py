from datetime import datetime

from pydantic import BaseModel, Field


class CreateUserProfileRequest(BaseModel):

    auth_user_id: str

    first_name: str = Field(
        min_length=1,
        max_length=50,
    )

    last_name: str = Field(
        min_length=1,
        max_length=50,
    )

    phone: str | None = None


class UpdateUserProfileRequest(BaseModel):

    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    phone: str | None = None


class UserResponse(BaseModel):
    id: str
    auth_user_id: str
    first_name: str
    last_name: str
    phone: str | None
    created_at: datetime
    updated_at: datetime