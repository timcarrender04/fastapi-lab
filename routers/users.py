from fastapi import APIRouter, Depends
from pydantic import BaseModel

from dependencies import get_current_user

# Every route on this router requires X-Token.
# Missing header is 422. Wrong token is 401. secret-token is allowed through.
router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
)


class UserIn(BaseModel):
    username: str


users: list[dict] = [
    {"id": 1, "username": "ada"},
    {"id": 2, "username": "linus"},
]
next_id = 3


# GET /users returns 200 and the user list, only with a valid token.
@router.get("")
def list_users():
    return users


# POST /users returns 201 and appends the body, only with a valid token.
@router.post("", status_code=201)
def create_user(user: UserIn):
    global next_id
    new_user = {"id": next_id, "username": user.username}
    next_id += 1
    users.append(new_user)
    return new_user
