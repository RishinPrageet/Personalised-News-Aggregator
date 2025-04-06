from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL
from backend.database.base import Base  # Updated import

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, pool_size=10,
    max_overflow=20, pool_timeout=60, pool_recycle=1800,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine, checkfirst=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()