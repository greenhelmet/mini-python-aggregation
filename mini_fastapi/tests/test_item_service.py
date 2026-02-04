import pytest
from app.services.item_service import create_item, _items, get_item_by_id
from app.schemas.item import ItemCreate

def setup_function():
    _items.clear()
    
def test_get_item_by_id_success():
    created = create_item(ItemCreate(item_name="apple"))

    result = get_item_by_id(created.id)

    assert result.id == created.id
    assert result.item_name == "apple"
    
def test_get_item_by_id_not_found():
    with pytest.raises(ValueError):
        get_item_by_id("not-exist-id")

    