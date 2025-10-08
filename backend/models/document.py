from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from utils.database import Base
import uuid
import enum

class DocumentTypeEnum(str, enum.Enum):
    setup = "setup"
    environment = "environment"
    deployment = "deployment"
    general = "general"

class Document(Base):
    __tablename__ = "documents"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(CHAR(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    type = Column(Enum(DocumentTypeEnum), nullable=True)
    created_by = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="documents")
