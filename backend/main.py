from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import Base, engine, SessionLocal
from utils.seed import seed_database
from routers import auth, projects, notes, tasks, documents
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DevNoteX API",
    description="Backend API for DevNoteX - Developer Workspace Platform",
    version="1.0.0"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        yield
    finally:
        db.close()
        
app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(notes.router)
app.include_router(tasks.router)
app.include_router(documents.router)

# @app.on_event("startup")
# async def startup_event():
#     logger.info("Creating database tables...")
#     Base.metadata.create_all(bind=engine)
#     logger.info("Database tables created successfully!")

#     logger.info("Seeding database...")
#     db = SessionLocal()
#     try:
#         seed_database(db)
#     finally:
#         db.close()

@app.get("/")
async def root():
    return {
        "message": "Welcome to DevNoteX API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
