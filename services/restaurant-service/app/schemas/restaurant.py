from datetime import datetime
from pydantic import BaseModel, Field


class CreateRestaurantRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    phone: str | None = None
    email: str | None = None
    address: str = Field(min_length=5, max_length=250)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    pincode: str = Field(min_length=4, max_length=10)
    latitude: float | None = None
    longitude: float | None = None


class UpdateRestaurantRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    phone: str | None = None
    email: str | None = None
    address: str | None = Field(default=None, min_length=5, max_length=250)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    state: str | None = Field(default=None, min_length=2, max_length=100)
    pincode: str | None = Field(default=None, min_length=4, max_length=10)
    latitude: float | None = None
    longitude: float | None = None
    is_open: bool | None = None


class RestaurantResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str
    city: str
    state: str
    pincode: str
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool
    is_open: bool
    created_at: datetime
    updated_at: datetime

  


class RestaurantListResponse(BaseModel):
    items: list[RestaurantResponse]
    page: int
    page_size: int
    total: int
    total_pages: int