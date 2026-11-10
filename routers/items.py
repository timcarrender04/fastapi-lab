from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])


class ItemIn(BaseModel):
    name: str
    price: float


# The list lives in this process. Stop uvicorn and it is gone. Postgres is next week.
items: list[dict] = [
    {"id": 1, "name": "notebook", "price": 3.50},
    {"id": 2, "name": "pencil", "price": 0.75},
]
next_id = 3


def _find(item_id: int) -> dict | None:
    for item in items:
        if item["id"] == item_id:
            return item
    return None


# GET /items returns 200 and every item currently in the list.
@router.get("")
def list_items():
    return items


# GET /items/{item_id} returns 200 for a known id and 404 when the id is missing.
@router.get("/{item_id}")
def read_item(item_id: int):
    item = _find(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# POST /items returns 201 and appends the body. A bad body is 422.
@router.post("", status_code=201)
def create_item(item: ItemIn):
    global next_id
    new_item = {"id": next_id, **item.model_dump()}
    next_id += 1
    items.append(new_item)
    return new_item


# PUT /items/{item_id} replaces name and price. Missing id is 404. A bad body is 422.
@router.put("/{item_id}")
def update_item(item_id: int, item: ItemIn):
    current = _find(item_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Item not found")
    current["name"] = item.name
    current["price"] = item.price
    return current


# DELETE /items/{item_id} returns 204 with an empty body. Missing id is 404.
@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    current = _find(item_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items.remove(current)
