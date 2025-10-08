from sqlalchemy.orm import Session
from models import User, Project, ProjectMember, RoleEnum
from utils.auth import get_password_hash
import logging

logger = logging.getLogger(__name__)

def seed_database(db: Session):
    try:
        existing_user = db.query(User).filter(User.email == "demo@devnotex.com").first()

        if existing_user:
            logger.info("Seed data already exists. Skipping...")
            return

        demo_user = User(
            email="demo@devnotex.com",
            hashed_password=get_password_hash("testpass"),
            full_name="Demo Admin"
        )

        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        logger.info(f"Created demo user: {demo_user.email}")

        demo_project = Project(
            name="DevNoteX Project",
            description="Demo project for the DevNoteX platform",
            created_by=demo_user.id
        )

        db.add(demo_project)
        db.commit()
        db.refresh(demo_project)

        logger.info(f"Created demo project: {demo_project.name}")

        demo_membership = ProjectMember(
            project_id=demo_project.id,
            user_id=demo_user.id,
            role=RoleEnum.admin
        )

        db.add(demo_membership)
        db.commit()

        logger.info(f"Added {demo_user.email} as admin to {demo_project.name}")
        logger.info("Seed data created successfully!")

    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        db.rollback()
        raise
