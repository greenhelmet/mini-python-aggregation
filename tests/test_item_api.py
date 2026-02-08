from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_item_by_id_api_400():
    response = client.get("/items/not-exist-id")

    assert response.status_code == 400
    
    body = response.json()
    assert body["type"] == "business_error"
    assert body["status"] == 400
    assert "detail" in body
    
def test_create_item_api_validation_error():
    response = client.post(
        "/items/",
        json={"wrong_field": "value"},
    )

    assert response.status_code == 422
    
    body = response.json()
    assert body["type"] == "validation_error"
    assert body["status"] == 422
    assert isinstance(body["detail"], list)