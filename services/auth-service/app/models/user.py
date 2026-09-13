from datetime import datetime, timezone
from beanie import Document
from pydantic import EmailStr, Field

from app.core.enums import UserRole


class User(Document):
    email: EmailStr
    password_hash: str
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone: str | None = Field(default=None, min_length=10, max_length=15)
    role: UserRole = UserRole.CUSTOMER
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"