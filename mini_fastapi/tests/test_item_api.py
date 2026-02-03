from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_item_by_id_api_404():
    response = client.get("/items/not-exist-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"