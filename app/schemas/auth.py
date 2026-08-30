from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(...,min_length=2,max_length=100,)
    email: EmailStr
    phone: str | None = Field(default=None,min_length=10,max_length=15,)
    password: str = Field( ..., min_length=8, max_length=72,)


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone: str | None = None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    email:EmailStr
    password:str    


class LoginResponse(BaseModel):
    access_token:str
    token_type:str="bearer"



class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=15,
    )        