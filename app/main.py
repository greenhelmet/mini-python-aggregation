from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.routers import items
from app.core.exceptions import (
    value_error_handler,
    request_validation_error_handler,
    unhandled_exception_handler,
)

app = FastAPI()

app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(items.router)