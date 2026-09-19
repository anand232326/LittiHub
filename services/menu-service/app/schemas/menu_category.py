from datetime import datetime
from pydantic import BaseModel, Field


class CreateMenuCategoryRequest(BaseModel):

    name: str = Field(min_length=2,max_length=100,)
    description: str | None = Field(default=None,max_length=500,)
    display_order: int = Field(default=0,ge=0,)



class UpdateMenuCategoryRequest(BaseModel):
    name: str | None = Field(default=None,min_length=2,max_length=100,)
    description: str | None = Field(default=None,max_length=500,)
    display_order: int | None = Field(default=None,ge=0,)




class MenuCategoryResponse(BaseModel):
    id: str
    restaurant_id: str
    name: str
    description: str | None
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime