import sqlite3

conn = sqlite3.connect("news_aggregator.db")
cursor = conn.cursor()

# Ensure table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS websites (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    url VARCHAR NOT NULL UNIQUE,
    topic VARCHAR NOT NULL
);
""")

# List of sports websites
sports_websites = [
    {"name": "ESPN", "url": "https://www.espn.com/espn/rss/news", "topic": "Sports"},
    {"name": "BBC Sport", "url": "http://feeds.bbci.co.uk/sport/rss.xml", "topic": "Sports"},
    {"name": "Sky Sports", "url": "https://www.skysports.com/rss/12040", "topic": "Sports"},
    {"name": "CBS Sports", "url": "https://www.cbssports.com/rss/headlines/", "topic": "Sports"},
    {"name": "FOX Sports", "url": "https://www.foxsports.com/feedout/syndicatedContent", "topic": "Sports"},
    {"name": "Yahoo Sports", "url": "https://sports.yahoo.com/rss/", "topic": "Sports"},


    {"name": "MLB News", "url": "https://www.mlb.com/feeds/news/rss.xml", "topic": "Sports"},
 
    {"name": "Formula 1", "url": "https://www.formula1.com/content/fom-website/en/latest/all.xml", "topic": "Sports"},
    {"name": "MMA Fighting", "url": "https://www.mmafighting.com/rss/current", "topic": "Sports"},

    {"name": "ESPN Cricinfo", "url": "https://www.espncricinfo.com/rss/content/story/feeds/0.xml", "topic": "Cricket"}
]
football_websites = [
  {
    "name": "BBC Football",
    "url": "http://feeds.bbci.co.uk/sport/football/rss.xml",
    "topic": "Sports"
  },

  {
    "name": "ESPN FC",
    "url": "https://www.espn.com/espn/rss/soccer/news",
    "topic": "Sports"
  },
  {
    "name": "The Guardian Football",
    "url": "https://www.theguardian.com/football/rss",
    "topic": "Sports"
  },
   {
    "name": "Football Italia",
    "url": "https://www.football-italia.net/rss",
    "topic": "Sports"
  }

]

# Insert into the table
for i, site in enumerate(football_websites, start=1):
    cursor.execute(
        "INSERT OR IGNORE INTO websites (id, name, url, topic) VALUES (?, ?, ?, ?)",
        (i+317, site["name"], site["url"], site["topic"])
    )

conn.commit()
conn.close()
