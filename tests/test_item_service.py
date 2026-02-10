import pytest

from app.services.item_service import (
    create_item,
    get_item_by_id,
    get_items,
    _items,
)
from app.schemas.item import ItemCreate
from app.schemas.user import User


def setup_function():
    _items.clear()


def fake_user():
    return User(
        id="user-1",
        username="test-user",
    )


def test_get_item_by_id_success():
    user = fake_user()
    created = create_item(ItemCreate(item_name="apple"), user)

    result = get_item_by_id(created.id, user)

    assert result.id == created.id
    assert result.item_name == "apple"


def test_get_item_by_id_not_found():
    user = fake_user()
    with pytest.raises(ValueError):
        get_item_by_id("not-exist-id", user)


def test_get_items_with_user():
    user = fake_user()

    create_item(ItemCreate(item_name="apple"), user)
    create_item(ItemCreate(item_name="banana"), user)

    items = get_items(user)

    assert len(items) == 2
    assert {item.item_name for item in items} == {"apple", "banana"}
