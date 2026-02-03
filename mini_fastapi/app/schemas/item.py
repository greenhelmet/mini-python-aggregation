from pydantic import BaseModel

class Item(BaseModel):
    id: str
    
class ItemCreate(BaseModel):
    name: str