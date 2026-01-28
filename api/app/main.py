import os
from fastapi import FastAPI, Depends#, HTTPException
from fastapi.staticfiles import StaticFiles
from app.database import get_db, engine, Base
from app.repository import TaskRepository
from app.schemas import TaskCreate#, TaskResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", version="1.0.0")

UI_ORIGINS = os.getenv("UI_ORIGINS", "")

origins = [o.strip() for o in UI_ORIGINS.split(",") if o]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "task-api",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "tasks": "/tasks",
            "docs": "/docs"
        }
    }

@app.post("/tasks")#, response_model=TaskResponse)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    return repo.add(task_data.title, task_data.status, task_data.dueDate)

@app.get("/tasks")#, response_model=[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    return repo.get()

@app.put("/tasks/{task_id}")
def update_task(task_id: str, task_data: TaskCreate, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    updated_task = repo.update(task_id, task_data.title, task_data.status, task_data.dueDate)
    if updated_task:
        return updated_task
    return {"error": "Task not found"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    repo.remove(task_id)
    return {"message": "Task deleted successfully"}