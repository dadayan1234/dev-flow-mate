from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from utils.database import get_db
from utils.auth import get_current_user_id
from models import Document, ProjectMember
from schemas import DocumentCreate, DocumentUpdate, DocumentResponse

router = APIRouter(prefix="/api/projects/{project_id}/documents", tags=["Documents"])

def check_member_access(project_id: str, user_id: str, db: Session):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id,
        ProjectMember.role.in_(["admin", "member"])
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this project"
        )

@router.get("", response_model=List[DocumentResponse])
async def get_documents(
    project_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project"
        )

    documents = db.query(Document).filter(Document.project_id == project_id).all()
    return documents

@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    project_id: str,
    doc_data: DocumentCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_member_access(project_id, user_id, db)

    new_document = Document(
        project_id=project_id,
        title=doc_data.title,
        content=doc_data.content,
        type=doc_data.type,
        created_by=user_id
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document

@router.get("/{doc_id}", response_model=DocumentResponse)
async def get_document(
    project_id: str,
    doc_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project"
        )

    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.project_id == project_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return document

@router.put("/{doc_id}", response_model=DocumentResponse)
async def update_document(
    project_id: str,
    doc_id: str,
    doc_data: DocumentUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_member_access(project_id, user_id, db)

    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.project_id == project_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    update_data = doc_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(document, key, value)

    db.commit()
    db.refresh(document)

    return document

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    project_id: str,
    doc_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_member_access(project_id, user_id, db)

    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.project_id == project_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    db.delete(document)
    db.commit()
