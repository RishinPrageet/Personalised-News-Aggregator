import sqlite3
import feedparser
from datetime import datetime

def fetch_and_store_news():
    # Connect to the SQLite database
    conn = sqlite3.connect("news_aggregator.db")
    cursor = conn.cursor()
    
    # Fetch all website records from the websites table
    cursor.execute("SELECT id, name, url, topic FROM websites")
    websites = cursor.fetchall()
    
    for website in websites:
        website_id, name, feed_url, topic = website
        print(f"Fetching news from '{name}' (Feed URL: {feed_url})")
        
        # Parse the RSS/Atom feed
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries:
            # Extract title, description (summary), link
            title = entry.get("title", None)
            description = entry.get("summary", None)
            link = entry.get("link", None)
            
            # Process published date if available
            published = None
            if "published_parsed" in entry and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6]).isoformat()
            
            # Attempt to extract an image URL (using media_content or links with image type)
            image = None
            if "media_content" in entry and len(entry.media_content) > 0:
                image = entry.media_content[0].get("url", None)
            else:
                for link_obj in entry.get("links", []):
                    if link_obj.get("type", "").startswith("image"):
                        image = link_obj.get("href", None)
                        break
            
            # Only insert if we have at least a title and a link.
            if title and link:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO news (title, description, link, image, published, website_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (title, description, link, image, published, website_id))
                except Exception as e:
                    print(f"Error inserting news item: {e}")
        
        # Commit changes after processing each feed
        conn.commit()
    
    conn.close()
    print("News fetching and storing complete.")

if __name__ == "__main__":
    fetch_and_store_news()
