from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from utils.database import get_db
from utils.auth import get_current_user_id
from models import Task, ProjectMember
from schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api/projects/{project_id}/tasks", tags=["Tasks"])

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

@router.get("", response_model=List[TaskResponse])
async def get_tasks(
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

    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    return tasks

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: str,
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_member_access(project_id, user_id, db)

    new_task = Task(
        project_id=project_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        assigned_to=task_data.assigned_to,
        due_date=task_data.due_date,
        created_by=user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    project_id: str,
    task_id: str,
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

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.project_id == project_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    project_id: str,
    task_id: str,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_member_access(project_id, user_id, db)

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.project_id == project_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    update_data = task_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    project_id: str,
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_member_access(project_id, user_id, db)

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.project_id == project_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()
