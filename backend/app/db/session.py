from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# For local development, using SQLite; update for production (e.g., PostgreSQL)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
