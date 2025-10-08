from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "backlog"
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskResponse(TaskBase):
    id: str
    project_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
