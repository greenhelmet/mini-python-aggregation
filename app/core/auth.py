from fastapi import Depends
from app.schemas.user import User
from app.core.logging import get_logger

logger = get_logger(__name__)

def get_token() -> str:
    logger.info("get_token dependency called")
    return "mock-token"

def get_current_user(
    token: str = Depends(get_token),
) -> User:
    logger.info("get_current_user dependency called")

    return User(
        username="mockuser",
        email="mock@example.com",
        full_name="Mock User",
        disabled=False,
    )
