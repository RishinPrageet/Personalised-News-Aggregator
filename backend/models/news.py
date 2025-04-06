from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.base import Base
from datetime import datetime

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    link = Column(String, unique=True, nullable=False)
    image = Column(String)
    published = Column(DateTime, default=datetime.utcnow)

    website_id = Column(Integer, ForeignKey('websites.id'), nullable=False)
    website = relationship('Website', back_populates='news_items')
    comments = relationship("Comment", back_populates="news", cascade="all, delete-orphan")
