from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings

def register_cors_middleware(app: FastAPI) -> None:
    """
    Configures CORS middleware for the FastAPI application
    """
    origins = [origin.strip() for origin in settings.ui_origins.split(",") if origin.strip()]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=r"https://.*\.vercel\.app",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )