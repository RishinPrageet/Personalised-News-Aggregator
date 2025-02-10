
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.models.user import User  # Import the User model
from backend.schemas.user import UserCreate,UserResponse
from backend.utilities.hashing import hash_password

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(user:UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)   
    db_user = User(email=user.email, username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    
    return db_user
