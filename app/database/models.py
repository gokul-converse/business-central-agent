from datetime import datetime, timezone
from sqlalchemy import DateTime, String, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.database.database import Base

class AgentSessionModel(Base):                                   # this Python class represents our PostgreSQL table.
    __tablename__ = "agent_sessions"

    session_id: Mapped[str] = mapped_column(String(255), primary_key = True)
    service_session_id: Mapped[str] = mapped_column(String(255), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone =True), default = datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone = True), default = datetime.utcnow)

class ConversationMessageModel(Base):
    __tablename__ = "conversation_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(255), ForeignKey("agent_sessions.session_id"), nullable=True, index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
