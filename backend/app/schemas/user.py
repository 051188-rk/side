from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    display_name: str
    role: str = "user"
    organization_id: Optional[str] = None
    firebase_uid: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    role: Optional[str] = None
    organization_id: Optional[str] = None
    is_active: Optional[bool] = None
    email_verified: Optional[bool] = None


class UserResponse(UserBase):
    id: str
    is_active: bool
    email_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    firebase_token: Optional[str] = None


class UserSignup(BaseModel):
    email: EmailStr
    password: str
    display_name: str
    organization_name: Optional[str] = None
