from pydantic import BaseModel

class Item(BaseModel):
    id: str
    name: str
    
class ItemCreate(BaseModel):
    name: str