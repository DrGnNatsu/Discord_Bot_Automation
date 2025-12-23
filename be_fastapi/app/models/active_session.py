# The Bot's Short-Term Memory (State Machine)
from sqlalchemy import Column, String, ForeignKey, JSON, DateTime, func

from app.db.session import Base


class ActiveSession(Base):
    __tablename__ = "active_sessions"

    # Composite Primary Key: A user can only be in ONE instance of a specific workflow
    user_id = Column(String, primary_key=True)
    workflow_id = Column(String, ForeignKey("workflows.id"), primary_key=True)

    current_state = Column(String, nullable=False) # e.g., 'start', 'awaiting_reason'
    variables = Column(JSON, default={})           # e.g., {"strikes": 1}
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())