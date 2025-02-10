from pydantic import BaseModel, EmailStr,Field,ConfigDict
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr  
    username: str = Field(..., min_length=3)  
    password: str = Field(..., min_length=6)

    model_config = ConfigDict(from_attributes=True)

class UserRequest(BaseModel):
    email: Optional[EmailStr] = None  
    username: Optional[str] = Field(default=None, min_length=3)   
    password: str = Field(..., min_length=6)

    model_config = ConfigDict(from_attributes=True)  
 

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)  
