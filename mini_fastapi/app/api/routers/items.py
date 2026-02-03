from typing import List
from fastapi import APIRouter, HTTPException

from app.schemas.item import Item, ItemCreate
from app.services.item_service import get_items, create_item, get_item_by_id

router = APIRouter()

@router.get("/items/", response_model=List[Item])
async def read_items():
    return get_items()

@router.get("/items/{item_id}", response_model=Item)
async def get_item_by_id_endpoint(item_id: str):
    try:
        return get_item_by_id(item_id)
    except ValueError:
        return HTTPException(status_code=404, detail="Item not found")

@router.post("/items/", response_model=Item)
async def create_item_endpoint(item: ItemCreate):
    return create_item(item)