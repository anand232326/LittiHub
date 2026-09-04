from pydantic import BaseModel,Field
from datetime import datetime
from typing import Generic, TypeVar


class RestaurantCreate(BaseModel):
    outlet_name: str
    phone: str
    address: str
    city: str
    locality: str
    pincode: str
    latitude: float | None = None
    longitude: float | None = None


class RestaurantResponse(BaseModel):
    id: str
    outlet_name: str
    phone: str
    address: str
    city: str
    locality: str
    pincode: str
    latitude: float | None
    longitude: float | None
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
    outlet_name: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    locality: str | None = None
    pincode: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool | None = None