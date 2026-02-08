from typing import List, Dict
from uuid import uuid4

from app.schemas.item import Item, ItemCreate
from app.core.logging import get_logger

logger = get_logger(__name__)

_items: list[Item] = []

def get_items() -> List[Item]:
    return _items

def create_item(data: ItemCreate) -> Item:
    logger.debug("Creating item", extra={"item_name": data.item_name})
    
    item_id = str(uuid4())
    item = Item(
        id=item_id,
        item_name=data.item_name,
    )
    _items.append(item)
    
    logger.info(
        "Item created",
        extra={
            "item_id": item.id,
            "items_count": len(_items),
        },
    )
    
    return item

def get_item_by_id(item_id: str) -> Item:
    logger.debug(
        "Searching item",
        extra={
            "item_id": item_id,
            "items_count": len(_items),
        },
    )
    
    for item in _items:
        if item.id == item_id:
            logger.debug("Item Found", extra={"item_id": item_id})
            return item
        
    logger.warning("Item not found", extra={"item_id": item_id})
    raise ValueError(f"Item not found: {item_id}")
    