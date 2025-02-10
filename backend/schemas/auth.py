from pydantic import BaseModel, EmailStr,Field,ConfigDict
from datetime import datetime
from typing import Optional

class token(BaseModel):
    access_token: str
    token_type: str