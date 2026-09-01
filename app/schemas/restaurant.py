from pydantic import BaseModel,Field
from datetime import datetime
from typing import Generic, TypeVar

class RestaurantCreate(BaseModel):
    name:str=Field(min_length=2,max_length=150,)
    phone:str=Field(default=None,min_length=10,max_length=15,)
    address:str=Field(min_length=5,max_length=300,)
    city:str=Field(min_length=2,max_length=100,)


class RestaurantResponse(BaseModel):
    id: str
    name: str
    phone: str | None
    address: str
    city: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


T=TypeVar("T")

class PaginatedResponse(BaseModel,Generic[T]):
    items:list[T]
    total:int
    page:int
    page_size:int
    total_pages:int


class RestaurantUpdate(BaseModel):
    name: str | None = Field(default=None,min_length=2,max_length=100,)
    phone: str | None = Field(default=None,min_length=10,max_length=15,)
    address: str | None = Field(default=None,min_length=5,max_length=200,)
    city: str | None = Field(default=None,min_length=2,max_length=100,)
    is_active: bool | None = None
