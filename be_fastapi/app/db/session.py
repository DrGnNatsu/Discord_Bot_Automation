import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "guild_flow.db")

# Use absolute path for SQLite
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

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
    