from uuid import uuid4
from fastapi import Request

from app.core.context import set_request_id, reset_request_id
from app.core.logging import get_logger

logger = get_logger("app.middleware")

async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid4())
    token = set_request_id(request_id)

    logger.info("request started", extra={"request_id": request_id})

    try:
        response = await call_next(request)
    finally:
        reset_request_id(token)

    response.headers["X-Request-ID"] = request_id
    logger.info("request finished", extra={"request_id": request_id})

    return response
