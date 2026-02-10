from fastapi import Header
from app.schemas.user import User
from app.core.logging import get_logger

logger = get_logger(__name__)

def _extract_token(authorization: str | None) -> str:
    if authorization is None:
        logger.warning("Authorization header missing")
        raise ValueError("Missing authorization header")

    # 토큰 없음, 형식 오류
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        logger.warning("Invalid authorization header format")
        raise ValueError("Invalid authorization header format")

    return token


def _load_user(token: str) -> User:
    # 사용자 없음
    if token != "mock-token":
        logger.warning("User not found for token")
        raise ValueError("User not found")

    return User(
        username="mockuser",
        email="mock@example.com",
        full_name="Mock User",
        disabled=False,
    )

def get_current_user(
    authorization: str | None = Header(default=None),
) -> User:
    logger.info("get_current_user dependency called")

    token = _extract_token(authorization)
    user = _load_user(token)
    
    return user