
from fastapi import APIRouter, Depends, HTTPException,Request,status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.models.user import User  # Import the User model
from backend.schemas.user import UserCreate,UserResponse
from backend.utilities.hashing import hash_password
from backend.routes.auth import get_current_user
from jinja2 import Environment, FileSystemLoader
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="frontend/templates")

router=APIRouter(prefix="/user")

@router.get("/profile")
def get_user_profile(request: Request,current_user: UserResponse = Depends(get_current_user)):
    print("near_end")
    user={}
    user["id"]=current_user.id
    user['username']=current_user.username
    print(user)
    print(current_user)
    return templates.TemplateResponse("profile.html", {"request": request, "user": current_user.model_dump()})

@router.get("/logout")
def get_user_profile(request: Request):
    
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie('access_token')
    return response
