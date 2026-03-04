"""FastAPI application entrypoint and top-level wiring."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.edge.routers.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", version="1.1.0")

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

app.include_router(tasks_router)


@app.get("/health")
async def health_check():
    """Return service liveness metadata."""
    return {
        "status": "healthy",
        "service": "task-api",
        "version": "1.1.0",
    }


@app.get("/")
async def root():
    """Return API descriptor and high-level endpoint discovery."""
    return {
        "message": "Task Management API",
        "version": "1.1.0",
        "endpoints": {
            "health": "/health",
            "tasks": "/tasks",
            "tasks_v1": "/v1/tasks",
            "docs": "/docs",
        },
    }
