class AuthenticationError(Exception):
    pass

class AuthorizationError(Exception):
    pass


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
    
    sanitized_errors = []
    for err in exc.errors():
        sanitized_errors.append(
            {
                "loc": err["loc"],
                "msg": err["msg"],
                "type": err["type"],
            }
        )
    
    return JSONResponse(
        status_code=422,
        content={
        "type": "validation_error",
        "title": "Invalid request payload",
        "status": 422,
        "detail": sanitized_errors,
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
    
def authentication_error_handler(
    request: Request, exc: AuthenticationError
) -> JSONResponse:
    logger.warning(
        "authentication failed",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    
    return JSONResponse(
        status_code=401,
        content={
            "type": "authentication_error",
            "title": "Authentication failed",
            "status": 401,
            "detail": str(exc),
        },
    )
    
def authorization_error_handler(
    request: Request, exc: AuthorizationError
) -> JSONResponse:
    logger.warning(
        "authorization failed",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    
    return JSONResponse(
        status_code=403,
        content={
            "type": "authorization_error",
            "title": "permission denied",
            "status": 403,
            "detail": str(exc),
        },
    )