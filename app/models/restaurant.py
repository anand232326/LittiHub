from datetime import datetime,timezone
from beanie import Document
from pydantic import Field


class Restaurant(Document):
    name:str=Field(min_length=2,max_length=150,)
    phone:str=Field(default=None,min_length=10,max_length=15,)
    address:str=Field(min_length=5,max_length=300,)
    city:str=Field(min_length=2,max_length=100,)
    is_active:bool=True
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
    updated_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))

    class Settings:
        name="Restaurant"