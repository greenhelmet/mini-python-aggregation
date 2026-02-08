from pydantic import BaseModel, Field, field_validator

class Item(BaseModel):
    id: str
    item_name: str
    
class ItemCreate(BaseModel):
    item_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_\- ]+$",
        description="아이템 이름 (2~50자, 영문/숫자/공백/-, _ 허용)"
    )
    
    @field_validator("item_name")
    @classmethod
    def forbid_reserved_words(cls, v: str) -> str:
        reserved = {"admin", "root", "system"}
        lower = v.lower()
        
        if any(word in lower for word in reserved):
            raise ValueError("item_name contains reserved word")
        
        return v