from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func,distinct
from datetime import datetime
from backend.database.db import get_db
from backend.models.user import User  # Import the User model
from backend.schemas.user import UserCreate, UserResponse
from backend.schemas.news import NewsResponse
from backend.models.news import News   
# Import the News model
from backend.models.website import Website
from typing import List
from backend.utilities.hashing import hash_password
from backend.routes.auth import get_current_user
from jinja2 import Environment, FileSystemLoader
from fastapi.templating import Jinja2Templates
import os 
import asyncio
import aiohttp
import sqlite3
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
import re
from backend.models.comment import Comment
from backend.schemas.comment import CommentCreate, CommentResponse


router = APIRouter(prefix="/news")
@router.on_event("startup")
async def startup_event():
    """Start the background news-fetching task on FastAPI startup."""
    asyncio.create_task(fetch_and_store_news())

@router.get("/today", response_model=List[NewsResponse])
def get_todays_news(db: Session = Depends(get_db)):
    # Get today's date in UTC (adjust if you need a different timezone)
    today_date = datetime.utcnow().date()
    # Use func.date() to compare only the date portion of the published datetime
    news_items = db.query(News).filter(func.date(News.published) == today_date).all()
    print(len(news_items))
    if not news_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No news available for today"
        )
    return news_items[:200] if len(news_items)>200 else news_items
@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    try:
        # Use SQLAlchemy's query interface with distinct to get unique topics.
        categories_query = db.query(distinct(Website.topic)).all()
        # categories_query returns a list of tuples, so extract the first element of each.
        categories = [category[0] for category in categories_query]
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/websites/{topic}")
def get_websites(topic: str, db: Session = Depends(get_db)):
    try:
        websites = db.query(Website).filter(Website.topic == topic).all()
        result = [
            {"id": site.id, "name": site.name, "url": site.url, "topic": site.topic}
            for site in websites
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{news_id}", response_model=NewsResponse)
def get_news_by_id(news_id: int, db: Session = Depends(get_db)):
    news_item = db.query(News).filter(News.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")
    return news_item

@router.post("/{news_id}/comments")
def add_comment(news_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    news_item = db.query(News).filter(News.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")

    new_comment = Comment(
        news_id=news_id,
        user_id=current_user.id,
        comment=comment.text
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment.to_dict()

@router.get("/{news_id}/comments")
def get_comments(news_id: int, db: Session = Depends(get_db)):
    res=[]
    comments = db.query(Comment).filter(Comment.news_id == news_id).all()
    for comment in comments:
        res.append(comment.to_dict())
    return res

DB_PATH = "db/news_aggregator.db"
DB_PATH = "db/news_aggregator.db"
C = 0

async def process_website(website, session):
    global C
    website_id, name, feed_url, topic = website
    print(f"Fetching news from '{name}' (Feed URL: {feed_url})")

    try:
        C += 1
        async with session.get(feed_url) as response:
            feed_data = await response.text()
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
        C -= 1
        return []

    feed = feedparser.parse(feed_data)
    news_entries = []

    for entry in feed.entries:
        title = entry.get("title")
        description = entry.get("summary")
        link = entry.get("link")
        published = None

        if "published_parsed" in entry and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6]).isoformat()

        image = None

        # Extract image logic
        if "media_content" in entry and entry.media_content:
            if isinstance(entry.media_content, list) and entry.media_content:
                image = entry.media_content[0].get("url")
            elif isinstance(entry.media_content, dict):
                image = entry.media_content.get("url")

        if not image and "enclosures" in entry:
            for enclosure in entry.enclosures:
                if "image" in enclosure.get("type", ""):
                    image = enclosure.get("url")
                    break

        if description:
            soup = BeautifulSoup(description, "html.parser")
            if not image:
                img_tag = soup.find("img")
                if img_tag and img_tag.has_attr("src"):
                    image = img_tag["src"]
            description = soup.get_text(separator=" ", strip=True)
            description = re.sub(r'\s+', ' ', description)

        # Append only if title, link, and image exist
        if title and link and image:
            news_entries.append((title, description, link, image, published, website_id))

    return news_entries


async def fetch_and_store_news():
    while True:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL;")  # Enable WAL mode for better concurrency
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, url, topic FROM websites")
        websites = cursor.fetchall()
        conn.close()

        all_news = []

        async with aiohttp.ClientSession() as session:
            tasks = [process_website(website, session) for website in websites]
            results = await asyncio.gather(*tasks)

            for news_list in results:
                all_news.extend(news_list)  # Collect all news items

        # Insert all news into DB using a single connection
        if all_news:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            for news_item in all_news:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO news (title, description, link, image, published, website_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, news_item)
                except sqlite3.OperationalError as e:
                    print(f"Database error: {e}")
            conn.commit()
            conn.close()

        print("News fetching and storing complete.")

        # Wait 24 hours (86400 seconds) before the next run
        await asyncio.sleep(86400)



