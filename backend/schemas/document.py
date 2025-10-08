from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    title: str
    content: Optional[str] = None
    type: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: str
    project_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
