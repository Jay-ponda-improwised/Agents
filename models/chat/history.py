from sqlalchemy import Column, String, Text, DateTime, UUID, ForeignKey, JSON
from sqlalchemy.sql import func
from config.database import Base
import uuid
from typing import Optional, Dict, Any


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    prompt = Column(Text, nullable=False)
    params = Column(JSON, nullable=True)
    model_id = Column(UUID(as_uuid=True), ForeignKey("models.id"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("chat_history.id"), nullable=True)
    request_route = Column(String, nullable=False)
    answers = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    archived_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<ChatHistory(id='{self.id}', prompt='{self.prompt[:50]}...')>"