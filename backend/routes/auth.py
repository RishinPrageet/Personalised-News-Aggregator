from fastapi import APIRouter, Depends, HTTPException, status, Request, Query,Form,BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.models.user import User  # Import the User model
from backend.schemas.user import UserCreate, UserResponse
from backend.schemas.auth import token
from backend.utilities.hashing import verify, hash_password
from backend.utilities.send_email import send_email
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr
from datetime import timedelta, datetime

from jose import jwt, JWTError
from urllib.parse import quote
import os
from dotenv import load_dotenv  
import requests
from jose import jwk
import jwt as pyjwt
import random
import string 

def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

router = APIRouter(prefix="/auth")





load_dotenv()  # Load environment variables from .env





SECRET_KEY = "gojo-TheStrongest"  # Change this to a secure, random string
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
templates = Jinja2Templates(directory="frontend/templates")
router.mount("/static", StaticFiles(directory="frontend/static"), name="static")

class customOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    email: Optional[EmailStr] = None

def create_verification_token(email: str, user_id: int, expires_delta: timedelta = timedelta(hours=24)) -> str:
    """
    Create a JWT token for email verification.
    The token includes an "action" claim so that we know it is for verifying email.
    """
    payload = {
        "sub": email,
        "id": user_id,
        "action": "verify_email",
        "exp": datetime.utcnow() + expires_delta,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_change_token(email: str, user_id: int, expires_delta: timedelta = timedelta(hours=24)) -> str:
    """
    Create a JWT token for email verification.
    The token includes an "action" claim so that we know it is for verifying email.
    """
    payload = {
        "sub": email,
        "id": user_id,
        "action": "change_password",
        "exp": datetime.utcnow() + expires_delta,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_form_data(
    email: Optional[EmailStr] = Form(default=None),
    username: Optional[str] = Form(default=None),
    password: Optional[str] = Form(default=None)
) -> UserCreate:
    return UserCreate(email=email, username=username, password=password)

@router.api_route("/register",methods=["GET","POST"])
async def register(request: Request, user: UserCreate=Depends(get_form_data) , db: Session = Depends(get_db)):
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
    
    verification_token = create_verification_token(db_user.email, db_user.id)
    verification_link = f"https://fleet-escargot-funky.ngrok-free.app/auth/verify_email?token={verification_token}"
    subject = "Verify your email address"
    body = f"Hi I am not scam,\n\nPlease verify your email by clicking on the following link:\n{verification_link}\n\nIf you did not sign up, please ignore this email."
    background_tasks = BackgroundTasks()
    background_tasks.add_task(send_email, db_user.email,subject=subject, body=body)

    message = "Successfully registered. Please verify your email and then log in."
    redirect_url = f"/login?message={quote(message)}"
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER,background=background_tasks)

@router.api_route("/forgot", methods=["GET", "POST"])
async def forgot_password(form_data: UserCreate = Depends(get_form_data),db: Session = Depends(get_db)):
    email = form_data.email
    user = db.query(User).filter(User.email==email).first()
    if not user:
        error="Account doesnt exist"
        redirect_url = f"/login?error={quote(error)}&form=forgot"
        response=RedirectResponse(url=redirect_url,status_code=status.HTTP_303_SEE_OTHER)
        return response
    verification_token = create_change_token(user.email, user.id)
    subject = "Account recovery"
    verification_link = f"https://fleet-escargot-funky.ngrok-free.app/auth/change_password?token={verification_token}"
    body = f"Hi I am not scam,\n\nPlease change your password by clicking on the following link:\n{verification_link}\n\nIf you did not sign up, please ignore this email."
    background_tasks = BackgroundTasks()
    background_tasks.add_task(send_email, user.email,subject=subject, body=body)
    message = "Sent a reset email"
    redirect_url = f"/login?message={quote(message)}"
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER,background=background_tasks)


@router.api_route("/change_password", methods=["GET", "POST"])
async def change_password(
    request: Request,
    token: Optional[str] = None,  
    db: Session = Depends(get_db)
):
    if request.method == "GET":
        token = request.query_params
        token=token.get('token')
        print(token)
        return RedirectResponse(url=f"/login?token={quote(token)}&form=change", status_code=status.HTTP_303_SEE_OTHER)

    # Process the POST request from the change password form.
    form = await request.form()
    new_password = form.get("password")
    token = form.get("token")  
    print(form)
    print(token)
    if not token or not new_password:
        error = "Missing token or new password."
        return RedirectResponse(url=f"/login?form=change&error={quote(error)}&token={quote(token or '')}", status_code=status.HTTP_303_SEE_OTHER)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("action") != "change_password":
            error = "Invalid token action."
            return RedirectResponse(url=f"/login?form=change&error={quote(error)}&token={quote(token or '')}", status_code=status.HTTP_303_SEE_OTHER)
        
        email, user_id = payload.get('sub'), payload.get('id')
        if not email or not user_id:
            error = "Invalid token payload."
            return RedirectResponse(url=f"/login?form=change&error={quote(error)}&token={quote(token or '')}", status_code=status.HTTP_303_SEE_OTHER)
    except Exception:
        error = "Invalid or expired token."
        return RedirectResponse(url=f"/login?form=change&error={quote(error)}&token={quote(token or '')}", status_code=status.HTTP_303_SEE_OTHER)

    user = db.query(User).filter(User.id == user_id, User.email == email).first()
    if not user:
        error = "User not found."
        return RedirectResponse(url=f"/login?form=change&error={quote(error)}&token={quote(token or '')}", status_code=status.HTTP_303_SEE_OTHER)

    # Update password
    user.password = hash_password(new_password)
    db.commit()

    message = "Password updated successfully!"
    return RedirectResponse(url=f"/login?message={quote(message)}", status_code=status.HTTP_303_SEE_OTHER)



    


@router.api_route("/token", methods=["GET", "POST"])
async def login(form_data: Annotated[customOAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db), error: str = Query(None)):
    user = await authenticate_user(form_data.username, form_data.username, form_data.password, db)
    if not user:
        error = "Invalid Credentials, Try Again"
        redirect_url = f"/login?error={quote(error)}"
        return RedirectResponse(url=redirect_url,status_code=status.HTTP_303_SEE_OTHER)
    if not user.is_verified:
        error = "Email not verified. Please check your inbox for the verification email."
        redirect_url = f"/login?error={quote(error)}"
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    token = create_access_token(user.username, user.id, timedelta(minutes=30))

    response = RedirectResponse(url="/user/profile", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    
    return response



async def authenticate_user(username, email, password, db: Session):
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


async def get_current_user(
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
    
GOOGLE_JWKS_URI = 'https://www.googleapis.com/oauth2/v3/certs'

async def get_google_public_keys():
    """Fetch Google's public keys for JWT verification."""
    try:
        response = requests.get(GOOGLE_JWKS_URI)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google public keys: {e}")
        return None


@router.api_route("/callback", methods=["POST", "GET"])
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth callback and decode credentials directly."""

    if request.method == "GET":
        credentials = request.query_params.get("credential") # Assuming 'credentials' is in query params
    elif request.method == "POST":
        form_data = await request.form()
        credentials = form_data.get("credential") # Assuming 'credentials' is in form data
        print(f"Form data received: {form_data}") # Debugging, remove in production
    print(credentials)
    if not credentials:
        raise HTTPException(status_code=400, detail="Credentials not provided")

    id_token = credentials # Rename for clarity

    try:
        public_keys_data = await get_google_public_keys()
        if not public_keys_data:
            raise HTTPException(status_code=500, detail="Failed to fetch Google public keys")

        # Get the key for verification based on 'kid' in the header
        headers = jwt.get_unverified_header(id_token)
        kid = headers.get('kid')
        if not kid:
            raise HTTPException(status_code=400, detail="JWT missing 'kid' header")

        public_key = None
        for key_data in public_keys_data.get('keys', []):
            if key_data['kid'] == kid:
                public_key = jwk.construct(key_data)
                break

        if not public_key:
            raise HTTPException(status_code=400, detail=f"Public key with kid '{kid}' not found")

        # Verify the JWT signature and claims securely
        decoded_payload = jwt.decode(
            id_token,
            public_key,
            algorithms=["RS256"], # Google uses RS256
            issuer=["https://accounts.google.com", "accounts.google.com"],
            # audience=YOUR_GOOGLE_CLIENT_ID  # IMPORTANT: Validate your Client ID here if needed
            options={"verify_signature": True, "verify_iss": True, "verify_aud": False, "verify_exp": True}
        )


        email = decoded_payload.get("email")
        username = decoded_payload.get("name") # Or construct from given_name, family_name

        print(f"Verified Email: {email}")
        print(f"Verified Username: {username}")

        
        user = db.query(User).filter(User.email == email).first()

        if not user:
            user = User(email=email, username=username, password=hash_password(generate_random_string(random.randint(6,14))))
            db.add(user)
            db.commit()
            db.refresh(user)
        jwt_token = create_access_token(user.username, user.id,expires_delta=timedelta(minutes=30 ))
        response = RedirectResponse(url="/user/profile", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error during Google OAuth callback (direct decode): {e}")
        raise HTTPException(status_code=500, detail="Google authentication failed (direct decode)")

@router.get("/verify_email")
async def verify_email(token: str, db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("action") != "verify_email":
            raise HTTPException(status_code=400, detail="Invalid token action")
        email = payload.get("sub")
        user_id = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token payload")
        
        user = db.query(User).filter(User.id == user_id, User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Mark the user as verified.
        user.is_verified = True
        db.commit()
        message= "Email verified successfully. You can now log in."
        redirect_url = f"/login?message={quote(message)}"
        response =RedirectResponse(url=redirect_url,status_code=status.HTTP_303_SEE_OTHER)
        return response
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")   

   


