from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    is_verified = Column(Boolean,default=False)

    # relationships = relationship("OtherModel", back_populates="user")
