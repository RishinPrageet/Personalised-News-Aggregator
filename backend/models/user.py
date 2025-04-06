# backend/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.base import Base
from backend.models.association import user_website

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    is_verified = Column(Boolean, default=False)
    websites = relationship('Website', secondary=user_website, back_populates='users')
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
