from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from uuid import uuid4

from app.api.routers import items
from app.core.context import set_request_id, reset_request_id
from app.core.exceptions import (
    value_error_handler,
    request_validation_error_handler,
    unhandled_exception_handler,
    authentication_error_handler,
    authorization_error_handler,
    AuthenticationError,
    AuthorizationError,
)

app = FastAPI()

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid4())
    token = set_request_id(request_id)
    
    try:
        response = await call_next(request)
    finally:
        reset_request_id(token)
        
    response.headers["X-Request-ID"] = request_id
    return response

app.add_exception_handler(AuthenticationError, authentication_error_handler)
app.add_exception_handler(AuthorizationError, authorization_error_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(items.router)