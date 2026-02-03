from typing import List
from fastapi import APIRouter

from app.schemas.item import Item, ItemCreate
from app.services.item_service import get_items, create_item

router = APIRouter()

@router.get("/items/", response_model=List[Item])
async def read_items():
    return get_items()

@router.post("/items/", response_model=Item)
async def create_item_endpoint(item: ItemCreate):
    return create_item(item)