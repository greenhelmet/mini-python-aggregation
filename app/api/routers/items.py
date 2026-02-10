from typing import List
from fastapi import APIRouter, Depends

from app.schemas.item import Item, ItemCreate
from app.schemas.user import User
from app.services.item_service import get_items, create_item, get_item_by_id
from app.core.logging import get_logger
from app.core.auth import get_current_user, get_token

logger = get_logger(__name__)

router = APIRouter()

@router.get("/items/", response_model=List[Item])
async def read_items(
    user: User = Depends(get_current_user),
    token: str = Depends(get_token),
):
    logger.info("GET /items requested",
                extra={"user": user.username},
    )
    
    items = get_items(user)
    
    logger.info(
        "GET /items succeded",
        extra={"items_count": len(items)},
    )
    return items

@router.get("/items/{item_id}", response_model=Item)
async def get_item_by_id_endpoint(
    item_id: str,
    user: User = Depends(get_current_user)
):
    logger.info(
            "GET /items/{item_id} requested",
            extra={"item_id": item_id, "user": user.username},
    )
    
    item = get_item_by_id(item_id, user)
        
    logger.info(
        "GET /items/{item_id} succeeded",
        extra={"item_id": item_id},
    )
    return item

@router.post("/items/", response_model=Item)
async def create_item_endpoint(
    item: ItemCreate,
    user: User = Depends(get_current_user)
):
    logger.info(
        "POST /items requested",
        extra={"item_name": item.item_name},
    )
    
    created_item = create_item(item, user)
    
    logger.info(
        "POST /items succeeded",
        extra={"item_id": created_item.id},
    )
    return created_item