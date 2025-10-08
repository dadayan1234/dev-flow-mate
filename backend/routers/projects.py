from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from utils.database import get_db
from utils.auth import get_current_user_id
from models import Project, ProjectMember, RoleEnum, Task, StatusEnum
from schemas import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectStats

router = APIRouter(prefix="/api/projects", tags=["Projects"])

def check_project_access(project_id: str, user_id: str, db: Session, required_role: str = None):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project"
        )

    if required_role and membership.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You need {required_role} role for this action"
        )

    return membership

@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    projects = db.query(Project).join(ProjectMember).filter(
        ProjectMember.user_id == user_id
    ).all()

    return projects

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        repo_url=project_data.repo_url,
        created_by=user_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    new_member = ProjectMember(
        project_id=new_project.id,
        user_id=user_id,
        role=RoleEnum.admin
    )

    db.add(new_member)
    db.commit()

    return new_project

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_project_access(project_id, user_id, db)

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_project_access(project_id, user_id, db, required_role="admin")

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    update_data = project_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_project_access(project_id, user_id, db, required_role="admin")

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

@router.get("/{project_id}/stats", response_model=ProjectStats)
async def get_project_stats(
    project_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    check_project_access(project_id, user_id, db)

    tasks_total = db.query(func.count(Task.id)).filter(
        Task.project_id == project_id
    ).scalar()

    tasks_completed = db.query(func.count(Task.id)).filter(
        Task.project_id == project_id,
        Task.status == StatusEnum.done
    ).scalar()

    return ProjectStats(
        tasks_total=tasks_total or 0,
        tasks_completed=tasks_completed or 0
    )
