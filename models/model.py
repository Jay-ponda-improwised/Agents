from sqlalchemy import Column, String, Text, DateTime, UUID, ForeignKey, JSON
from sqlalchemy.sql import func
from config.database import Base
import uuid


class Model(Base):
    __tablename__ = "models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    model_name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<Model(id='{self.id}', model_name='{self.model_name}')>"