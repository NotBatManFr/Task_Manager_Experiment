from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings

def register_cors_middleware(app: FastAPI) -> None:
    """
    Configures CORS middleware for the FastAPI application
    """
    # origins: list[str] = [origin.strip() for origin in settings.cors_origins if origin.strip()]
    
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=["*"],
        # allow_credentials=False,
        # allow_origin_regex=r"https://.*\.vercel\.app",
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        # allow_methods=["GET, POST, PUT, DELETE"],
        # allow_headers=["application/json"],
        allow_headers=["*"],
        allow_methods=["*"],
    )