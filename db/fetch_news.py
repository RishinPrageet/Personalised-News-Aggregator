import asyncio
import aiohttp
import sqlite3
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
import re

DB_PATH = "db/news_aggregator.db"
C=0
async def fetch_feed(session, url):
    async with session.get(url) as response:
        return await response.text()

async def process_website(website, session, cursor):
    global C
    website_id, name, feed_url, topic = website
    print(f"Fetching news from '{name}' (Feed URL: {feed_url})")
    try:
        C+=1
        feed_data = await fetch_feed(session, feed_url)
        
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
        C-=1
        return

    feed = feedparser.parse(feed_data)
    
    for entry in feed.entries:
        title = entry.get("title")
        description = entry.get("summary")
        link = entry.get("link")
        published = None
        if "published_parsed" in entry and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6]).isoformat()

        image = None

        # Check media_content
        if "media_content" in entry and entry.media_content:
            if isinstance(entry.media_content, list) and entry.media_content:
                image = entry.media_content[0].get("url")
            elif isinstance(entry.media_content, dict):
                image = entry.media_content.get("url")

        # Check enclosure
        if not image and "enclosures" in entry:
            for enclosure in entry.enclosures:
                if "image" in enclosure.get("type", ""):
                    image = enclosure.get("url")
                    break

        # Extract from description if no image found
        if description:
            soup = BeautifulSoup(description, "html.parser")
            if not image:
                img_tag = soup.find("img")
                if img_tag and img_tag.has_attr("src"):
                    image = img_tag["src"]
            description = soup.get_text(separator=" ", strip=True)
            description = re.sub(r'\s+', ' ', description)

        # Store only if title, link, and image exist
        if title and link and image:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO news (title, description, link, image, published, website_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (title, description, link, image, published, website_id))
            except Exception as e:
                print(f"Error inserting news item: {e}")

async def fetch_and_store_news_async():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get websites from the database.
    cursor.execute("SELECT id, name, url, topic FROM websites")
    websites = cursor.fetchall()

    async with aiohttp.ClientSession() as session:
        tasks = [process_website(website, session, cursor) for website in websites]
        await asyncio.gather(*tasks)

    conn.commit()
    conn.close()
    print("News fetching and storing complete.")
    print(C)

if __name__ == "__main__":
    asyncio.run(fetch_and_store_news_async())
