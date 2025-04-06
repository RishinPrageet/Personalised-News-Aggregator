import os

# Database URL for SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db/news_aggregator.db")
