# import os
from fastapi import FastAPI, Depends#, HTTPException
from fastapi.staticfiles import StaticFiles
from app.database import get_db, engine, Base
from app.repository import TaskRepository
from app.schemas import TaskCreate#, TaskResponse
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/tasks")#, response_model=TaskResponse)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    return repo.add(task_data.title, task_data.status)

@app.get("/tasks")#, response_model=[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    return repo.get()

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    repo.remove(task_id)
