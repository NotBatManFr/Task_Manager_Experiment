from fastapi import FastAPI

from src.infrastructure.lifecycle import lifespan
from src.routers import tasks as tasks_router, system as system_router
from src.exceptions.exception_handlers import register_exception_handlers
from middleware.cors import register_cors_middleware

app: FastAPI = FastAPI(
    title="Tasks API",
    description="API for managing tasks",
    version="1.1.0",
    lifespan=lifespan)

register_cors_middleware(app)
register_exception_handlers(app)

app.include_router(system_router.router)
app.include_router(tasks_router.router)