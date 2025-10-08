from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from utils.database import Base
import uuid
import enum

class Project(Base):
    __tablename__ = "projects"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    repo_url = Column(String(500), nullable=True)
    created_by = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")

class RoleEnum(str, enum.Enum):
    admin = "admin"
    member = "member"
    viewer = "viewer"

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(CHAR(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="members")
