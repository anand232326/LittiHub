from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class User(Document):

    auth_user_id: str = Field(
        unique=True
    )

    first_name: str

    last_name: str

    phone: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "users"