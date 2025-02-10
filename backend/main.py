from fastapi import FastAPI, Depends
from backend.routes import users, auth
from backend.database.db import engine, Base
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
from jinja2 import Environment, FileSystemLoader

# Create FastAPI app
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include the routers for users and authentication
app.include_router(users.router)
app.include_router(auth.router)

# Set up Jinja2 with whitespace control
env = Environment(
    loader=FileSystemLoader('frontend/templates'),
    trim_blocks=True,  # Remove leading newlines for blocks
    lstrip_blocks=True,  # Remove leading spaces before blocks
    autoescape=True,  # Automatically escape the output for safety
)

# Initialize FastAPI's Jinja2Templates with the custom environment
templates = Jinja2Templates( env=env)

# Serve static files like CSS, images, etc.
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Endpoint to serve login page
@app.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
