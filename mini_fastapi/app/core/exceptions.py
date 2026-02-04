from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import get_logger


logger = get_logger(__name__)


def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    logger.warning(
        "Business error occurred",
        extra={"error": str(exc), "path": request.url.path},
    )
    
    return JSONResponse(
        status_code=400,
        content={
        "type": "business_error",
        "title": "Invalid domain operation",
        "status": 400,
        "detail": str(exc),
        },
    )
    
def request_validation_error_handler(
    request: Request, exc: RequestValidationError
    ) -> JSONResponse:
    logger.info(
        "Request validation failed",
        extra={"error": exc.errors(), "path": request.url.path},
    )
    
    return JSONResponse(
        status_code=422,
        content={
        "type": "validation_error",
        "title": "Invalid request payload",
        "status": 422,
        "detail": exc.errors(),
        },
    )
    
def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.error(
        "unhandled exception occurred",
        exc_info=exc,
        extra={"path": request.url.path},
    )
    
    return JSONResponse(
        status_code=500,
        content={
        "type": "internal_error",
        "title": "Internal server error",
        "status": 500,
        "detail": "Unexcepted error occurred",
        },
    )