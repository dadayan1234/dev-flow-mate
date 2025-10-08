from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from utils.database import get_db
from utils.auth import get_current_user_id
from models import Note, ProjectMember
from schemas import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(prefix="/api/projects/{project_id}/notes", tags=["Notes"])

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

@router.get("", response_model=List[NoteResponse])
async def get_notes(
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

    notes = db.query(Note).filter(Note.project_id == project_id).all()
    return notes

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    project_id: str,
    note_data: NoteCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_member_access(project_id, user_id, db)

    new_note = Note(
        project_id=project_id,
        title=note_data.title,
        content=note_data.content,
        created_by=user_id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    project_id: str,
    note_id: str,
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

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.project_id == project_id
    ).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    project_id: str,
    note_id: str,
    note_data: NoteUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_member_access(project_id, user_id, db)

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.project_id == project_id
    ).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    update_data = note_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)

    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    project_id: str,
    note_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_member_access(project_id, user_id, db)

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.project_id == project_id
    ).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()
