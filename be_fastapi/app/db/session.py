from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the database file path. 
DATABASE_URL = "sqlite:///./database/guild_flow.db"

# connect_args={"check_same_thread": False} is CRITICAL for SQLite + FastAPI/Discord
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI to access the DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    