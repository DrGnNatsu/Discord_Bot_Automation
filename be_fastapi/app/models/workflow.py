# The Blueprints defined by Admins
from sqlalchemy import Column, String, Text, JSON, Boolean, DateTime, func

from app.db.session import Base
from app.models.admin_user import generate_uuid


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(String, primary_key=True, default=generate_uuid) # UUID for internal stability
    name = Column(String, unique=True, nullable=False)           # Unique name (e.g., 'anti_spam')
    trigger_event = Column(String, nullable=False, index=True)   # Indexed for speed

    source_code = Column(Text, nullable=True)     # RAW DSL: What the admin typed in Monaco
    compiled_json = Column(JSON, nullable=False)  # MACHINE CODE: What the bot executes

    is_active = Column(Boolean, default=True)   # Soft Delete
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
