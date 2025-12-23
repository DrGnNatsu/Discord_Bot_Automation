from sqlalchemy import Column, String

from app.db.session import Base
from app.utils.generate_id import generate_uuid


# --- 1. ADMIN USERS ---
# Stores login info for your React Dashboard
class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # Store Hashed passwords, never plain text!
    # discord_id = Column(String, nullable=True)     # Optional: For "Login with Discord"
