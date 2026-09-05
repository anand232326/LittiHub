from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class MenuCategoryCreate(BaseModel):


    restaurant_id: str

    name: str = Field(
    min_length=2,
    max_length=100,
    )

    description: str | None = Field(
    default=None,
    max_length=500,
    )


class MenuCategoryUpdate(BaseModel):


    name: str | None = Field(
    default=None,
    min_length=2,
    max_length=100,
    )

    description: str | None = Field(
    default=None,
    max_length=500,
    )

    is_active: bool | None = None


class MenuCategoryResponse(BaseModel):


    id: str

    restaurant_id: str

    name: str
    description: str | None

    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
    from_attributes=True
    )

