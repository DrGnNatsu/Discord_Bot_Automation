from fastapi import Request
from fastapi.responses import JSONResponse
from app.exception.base_exception import AppException


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "error_code": exc.__class__.__name__,  # Optional: helps frontend debug
            "detail": exc.detail
        },
    )