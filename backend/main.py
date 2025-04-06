from fastapi import FastAPI, Depends, status
from fastapi.responses import RedirectResponse
from backend.routes import users, auth, news, chatbot  # Import the chatbot router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
from jinja2 import Environment, FileSystemLoader
from backend.schemas.user import UserResponse
from backend.routes.auth import get_current_user
import os
from dotenv import load_dotenv

load_dotenv()

# Create FastAPI app
app = FastAPI()
SECRET_KEY = os.getenv("SECRET_KEY")

# Include the routers for users and authentication
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(news.router)
app.include_router(chatbot.router)  # Include the chatbot router

# Set up Jinja2 with whitespace control
env = Environment(
    loader=FileSystemLoader('frontend/templates'),
    trim_blocks=True,  # Remove leading newlines for blocks
    lstrip_blocks=True,  # Remove leading spaces before blocks
    autoescape=True,  # Automatically escape the output for safety 
)

# Initialize FastAPI's Jinja2Templates with the custom environment
templates = Jinja2Templates(env=env)
react_template = Jinja2Templates(directory='frontend/react-app/newsaggregation/dist')

# Serve static files like CSS, images, etc.
react_app_path = os.path.join("frontend", "react-app", "newsaggregation", "dist", "assets")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/assets", 
    StaticFiles(directory=react_app_path, html=True), 
    name="react_app")

@app.get("/")
def get_login_page(request: Request, error: str = None, message: str = None):
    redirect_url = f"/login"
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)

# Endpoint to serve login page
@app.api_route("/login", response_class=HTMLResponse, methods=["GET", "POST"])
def get_login_page(request: Request, error: str = None, message: str = None, token: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error, "message": message, "token": token})

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str, current_user: UserResponse = Depends(get_current_user)):
    user = {}
    user["id"] = current_user.id
    user['username'] = current_user.username
    return react_template.TemplateResponse("index.html", {"request": request, "user": user})
