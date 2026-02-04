from pydantic import BaseModel

class Item(BaseModel):
    id: str
    item_name: str
    
class ItemCreate(BaseModel):
    item_name: str