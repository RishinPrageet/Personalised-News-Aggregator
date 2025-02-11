from fastapi import APIRouter, Depends, HTTPException, status, Request, Query,Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.models.user import User  # Import the User model
from backend.schemas.user import UserCreate, UserResponse
from backend.schemas.auth import token
from backend.utilities.hashing import verify, hash_password
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr
from datetime import timedelta, datetime
from jose import jwt, JWTError
from urllib.parse import quote

router = APIRouter(prefix="/auth")

SECRET_KEY = "gojo-TheStrongest"  # Change this to a secure, random string
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
templates = Jinja2Templates(directory="frontend/templates")
router.mount("/static", StaticFiles(directory="frontend/static"), name="static")

class customOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    email: Optional[EmailStr] = None


def get_form_data(
    email: Optional[EmailStr] = Form(default=None),
    username: Optional[str] = Form(default=None),
    password: Optional[str] = Form(default=None)
) -> UserCreate:
    return UserCreate(email=email, username=username, password=password)

@router.api_route("/register",methods=["GET","POST"])
def register(request: Request, user: UserCreate=Depends(get_form_data) , db: Session = Depends(get_db)):
    if request.method == "GET":
        redirect_url = f"/login?form=register"
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        error = "Username already taken"
        redirect_url = f"/login?error={quote(error)}&form=register"
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        error = "Account already exists"
        redirect_url = f"/login?error={quote(error)}&form=register"
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    message = "Succesfully registered, Please login"
    redirect_url = f"/login?message={quote(message)}"
    return RedirectResponse(url=redirect_url,status_code=status.HTTP_303_SEE_OTHER)




@router.api_route("/token", methods=["GET", "POST"])
def login(form_data: Annotated[customOAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db), error: str = Query(None)):
    user = authenticate_user(form_data.username, form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(user.username, user.id, timedelta(minutes=30))

    # Set the redirect status code to 303 to convert the subsequent request to GET.
    response = RedirectResponse(url="/user/profile", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    
    return response


def authenticate_user(username, email, password, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        user = db.query(User).filter(User.email == email).first()

    if not user:
        return False

    hashed = user.password
    if not verify(password, hashed):
        return False

    return user


def create_access_token(username: str, id: int, expires_delta: timedelta):
    to_encode = {
        "sub": username,  # The subject (typically user identifier)
        "id": id,
        "exp": datetime.utcnow() + expires_delta  # Expiry time
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    # Remove the "Bearer " prefix if it exists.
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]
    return token


def get_current_user(
    token: str = Depends(get_token_from_cookie),
    db: Session = Depends(get_db)
) -> UserResponse:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(user)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
