"""
Utility endpoints for service health and discoverability
These have no business logic and no database dependency
"""

from fastapi import APIRouter

router: APIRouter = APIRouter(tags=["System"])

@router.get("/health", 
            summary="Health Check", 
            description="Endpoint to check if the service is running")
async def health_check():
    """
    Lightweight endpoint for monitoring service health. Returns basic status info.
    """
    return {
        "status": "healthy",
        "service": "task-api",
        "version": "1.1.0"
    }

@router.get("/", 
            summary="API Root",
            description="Root endpoint providing basic info about the API")
async def root():
    """
    Returns available endpoints group
    """
    return {
        "message": "Task Management API",
        "version": "1.1.0",
        "endpoints": {
            "health": "/health",
            "tasks": "/tasks"
        }
    }