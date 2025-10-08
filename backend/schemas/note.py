from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteResponse(NoteBase):
    id: str
    project_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
