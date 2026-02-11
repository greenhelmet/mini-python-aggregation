import logging
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.middleware import request_id_middleware


def create_test_app() -> FastAPI:
    app = FastAPI()

    app.middleware("http")(request_id_middleware)

    @app.get("/ping")
    async def ping():
        return {"ok": True}

    return app


def test_request_id_header_is_attached():
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/ping")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers

    request_id = response.headers["X-Request-ID"]
    assert isinstance(request_id, str)
    assert len(request_id) > 0


def test_request_start_and_end_logging(caplog):
    app = create_test_app()
    client = TestClient(app)

    caplog.set_level(logging.INFO)

    client.get("/ping")

    messages = [record.message for record in caplog.records]

    assert any("request started" in msg for msg in messages)
    assert any("request finished" in msg for msg in messages)
