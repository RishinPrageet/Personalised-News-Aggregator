from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.models.user import User  # Import the User model
from backend.schemas.user import UserCreate,UserResponse
from backend.schemas.auth import token
from backend.utilities.hashing import verify
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel, EmailStr
from datetime import timedelta , datetime

router = APIRouter()

class customOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    email : EmailStr

@router.post("/token",response_model=token)
def login(form_data: Annotated[customOAuth2PasswordRequestForm,Depends()],db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username,form_data.email,form_data.password,db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_acces_token

def authenticate_user(username, email, password, db: Session ):
    user=db.query(User).filter(User.username==username or User.email==email).first()
    if not user :
        return False
    hashed=user.password
    if not verify(password,hashed):
        return False
    return user
def create_acces_token(username:str , id: int , expires_delta: timedelta):
    to_encode = {
        "sub": username,  # The subject (typically user identifier)
        "id": id,
        "exp": datetime.utcnow() + expires_delta  # Expiry time
    }
    # Encode the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt