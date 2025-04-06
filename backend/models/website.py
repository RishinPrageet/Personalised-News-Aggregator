
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.db import Base
from backend.models.association import user_website


class Website(Base):
    __tablename__ = 'websites'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)            # e.g., "ESPN", "BBC News"
    url = Column(String, unique=True, nullable=False)  # Website URL (or feed URL)
    topic = Column(String, nullable=False)             # e.g., "sports", "world", "technology"
    users = relationship('User', secondary=user_website, back_populates='websites') 
    news_items = relationship('News', back_populates='website')