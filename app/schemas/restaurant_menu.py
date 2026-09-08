
from datetime import datetime
from pydantic import BaseModel


class RestaurantMenuItemResponse(BaseModel):
    id: str
    name: str
    description: str | None
    price: float
    image_url: str | None
    is_available: bool


class RestaurantMenuCategoryResponse(BaseModel):
    id: str
    name: str
    description: str | None
    items: list[RestaurantMenuItemResponse]


class RestaurantMenuRestaurantResponse(BaseModel):
    id: str
    outlet_name: str
    address: str
    city: str
    locality: str


class RestaurantMenuResponse(BaseModel):
    restaurant: RestaurantMenuRestaurantResponse
    categories: list[RestaurantMenuCategoryResponse]

