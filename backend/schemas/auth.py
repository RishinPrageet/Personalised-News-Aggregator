from pydantic import BaseModel, EmailStr,Field,ConfigDict
from fastapi import Form
from datetime import datetime
from typing import Optional

class token(BaseModel):
    access_token: str
    token_type: str

class Form(BaseModel):
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),