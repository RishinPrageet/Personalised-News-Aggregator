from pydantic import BaseModel, EmailStr,Field,ConfigDict
from fastapi import Form
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: Optional[EmailStr] = Form(default=None)
    username: Optional[str] = Form(default=None)
    password: Optional[str] = Form(default=None)

    model_config = ConfigDict(from_attributes=True)

class UserRequest(BaseModel):
    email: Optional[EmailStr] = None  
    username: Optional[str] = Field(default=None, min_length=3)   
    password: str = Field(..., min_length=6)

    model_config = ConfigDict(from_attributes=True)  
 

class UserResponse(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    username: str
    created_at: datetime
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)  
