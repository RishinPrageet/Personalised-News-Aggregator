# backend/models/association.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from backend.database.db import Base

user_website = Table(
    'user_website',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('website_id', Integer, ForeignKey('websites.id'), primary_key=True)
)
read_later = Table(
    'read_later',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('news_id', Integer, ForeignKey('news.id'), primary_key=True)
)
