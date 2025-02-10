from fastapi import FastAPI, Depends
from backend.routes import users  
from backend.database.db import engine, Base

# Create FastAPI app
app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(users.router)