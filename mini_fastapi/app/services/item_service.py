from typing import List, Dict
from uuid import uuid4

from app.schemas.item import Item, ItemCreate

_items: list[Item] = []

def get_items() -> List[Item]:
    return _items

def create_item(data: ItemCreate) -> Item:
    item_id = str(uuid4())
    item = Item(
        id=item_id,
        name=data.name,
    )
    _items.append(item)
    return item

def get_item_by_id(item_id: str) -> Item:
    for item in _items:
        if item.id == item_id:
            return item
    raise ValueError(f"Item not found: {item_id}")
    