"""
Translates domain exceptions into HTTP responses
"""

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from src.exceptions.exceptions import TaskNotFoundException, TaskDeleteError

def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers custom exception handlers for domain-specific errors
    """
    @app.exception_handler(TaskNotFoundException)
    async def task_not_found_exception_handler(request: Request, # type: ignore[arg-type]
                                                exc: TaskNotFoundException
                                                ) -> JSONResponse: 
        """
        Translate TaskNotFoundException into a 404 Not Found response
        """
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )

    @app.exception_handler(TaskDeleteError)
    async def task_delete_error_exception_handler(request: Request, # type: ignore[arg-type]
                                                  exc: TaskDeleteError
                                                  ) -> JSONResponse: 
        """
        Translate TaskDeleteError into a 500 Internal Server Error response
        """
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)}
        )