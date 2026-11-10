import pytest
from fastapi.testclient import TestClient

from main import app
from routers import items as items_router

client = TestClient(app)

SEED = [
    {"id": 1, "name": "notebook", "price": 3.50},
    {"id": 2, "name": "pencil", "price": 0.75},
]


@pytest.fixture(autouse=True)
def reset_items():
    items_router.items.clear()
    items_router.items.extend(dict(item) for item in SEED)
    items_router.next_id = 3
    yield


def test_item_crud_round_trip():
    created = client.post("/items", json={"name": "eraser", "price": 1.25})
    assert created.status_code == 201
    assert created.json() == {"id": 3, "name": "eraser", "price": 1.25}

    listed = client.get("/items")
    assert listed.status_code == 200
    assert created.json() in listed.json()

    fetched = client.get("/items/3")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "eraser"

    updated = client.put("/items/3", json={"name": "eraser pack", "price": 2.0})
    assert updated.status_code == 200
    assert updated.json() == {"id": 3, "name": "eraser pack", "price": 2.0}

    deleted = client.delete("/items/3")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get("/items/3").status_code == 404


def test_missing_item_is_404():
    assert client.get("/items/99").status_code == 404
    assert client.put("/items/99", json={"name": "nope", "price": 1.0}).status_code == 404
    assert client.delete("/items/99").status_code == 404


def test_bad_body_is_422():
    missing_price = client.post("/items", json={"name": "Widget"})
    assert missing_price.status_code == 422

    bad_price = client.post("/items", json={"name": "Widget", "price": "free"})
    assert bad_price.status_code == 422
