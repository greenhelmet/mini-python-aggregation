from typing import List
from fastapi import APIRouter, HTTPException

from app.schemas.item import Item, ItemCreate
from app.services.item_service import get_items, create_item, get_item_by_id
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/items/", response_model=List[Item])
async def read_items():
    logger.info("GET /items requested")
    
    items = get_items()
    
    logger.info(
        "GET /items succeded",
        extra={"items_count": len(items)},
    )
    return items

@router.get("/items/{item_id}", response_model=Item)
async def get_item_by_id_endpoint(item_id: str):
    logger.info(
            "GET /items/{item_id} requested",
            extra={"item_id": item_id},
    )
    try:
        item = get_item_by_id(item_id)
        
        logger.info(
            "GET /items/{item_id} succeeded",
            extra={"item_id": item_id},
        )
        return item
    
    except ValueError:
        logger.error(
            "GET /items/{item_id} failed: item not found",
            extra={"item_id": item_id},
        )
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/items/", response_model=Item)
async def create_item_endpoint(item: ItemCreate):
    logger.info(
        "POST /items requested",
        extra={"item_name": item.item_name},
    )
    
    created_item = create_item(item)
    
    logger.info(
        "POST /items succeeded",
        extra={"item_id": created_item.id},
    )
    return created_item