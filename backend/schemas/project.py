from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    repo_url: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    repo_url: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectStats(BaseModel):
    tasks_total: int
    tasks_completed: int

class ProjectMemberBase(BaseModel):
    user_id: str
    role: str

class ProjectMemberCreate(ProjectMemberBase):
    pass

class ProjectMemberResponse(ProjectMemberBase):
    id: str
    project_id: str
    joined_at: datetime

    class Config:
        from_attributes = True
