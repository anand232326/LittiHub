from datetime import datetime, timezone
from app.core.enums import UserRole
from beanie import Document
from pydantic import EmailStr, Field


class User(Document):

    full_name: str = Field(min_length=2,max_length=100,)
    email: EmailStr
    phone: str | None = Field(default=None,min_length=10,max_length=15,)
    hashed_password: str
    role: UserRole = UserRole.CUSTOMER
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"



        