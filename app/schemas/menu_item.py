from datetime import datetime
from pydantic import BaseModel, Field
from app.utils.pagination import PaginationResponse


class MenuItemCreate(BaseModel):
    restaurant_id:str
    category_id:str
    name:str=Field(min_length=2,max_length=100)
    description:str | None=Field(default=None,max_length=500,)
    price:float=Field(gt=0,)
    image_url:str | None=None



class MenuItemUpdate(BaseModel):
    name: str | None = Field(default=None,min_length=2,max_length=100,)
    description: str | None = Field(default=None,max_length=500,)
    price: float | None = Field(default=None,gt=0,)
    image_url: str | None = None
    is_available: bool | None = None
    is_active: bool | None = None



class MenuItemResponse(BaseModel):
    id: str
    restaurant_id: str
    category_id: str
    name: str
    description: str | None
    price: float
    image_url: str | None
    is_available: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


class MenuItemListResponse(BaseModel): 
    items: list[MenuItemResponse] 
    pagination: PaginationResponse    