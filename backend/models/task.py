from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from utils.database import Base
import uuid
import enum

class StatusEnum(str, enum.Enum):
    backlog = "backlog"
    todo = "todo"
    in_progress = "in_progress"
    review = "review"
    done = "done"

class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(CHAR(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.backlog)
    priority = Column(Enum(PriorityEnum), nullable=True)
    assigned_to = Column(CHAR(36), ForeignKey("users.id"), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")
