from typing import List, Dict
from uuid import uuid4

from app.schemas.item import Item, ItemCreate

_items: Dict[str, Item] = {}

def get_items() -> List[Item]:
    return list(_items.values())

def create_item(data: ItemCreate) -> Item:
    item_id = str(uuid4())
    item = Item(id=item_id)
    _items[item_id] = item
    return item