from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from users.exceptions import UserNotFound
from users.models import User, UserCreate
from utils.pagination import pagination

users_db: Dict[int, User] = {}
user_id_counter = 0

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_users(
    pagination: Annotated[Dict[str, int], Depends(pagination)],
) -> List[User]:
    skip, limit = pagination["skip"], pagination["limit"]
    return list(users_db.values())[skip : skip + limit]


@router.post("/")
async def create_user(user: UserCreate) -> User:
    global user_id_counter
    new_user = User.from_create(id=user_id_counter, user=user)
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user


@router.put("/{user_id}")
async def update_user(user_id: int, user: UserCreate) -> User:
    if user_id not in users_db:
        raise UserNotFound()

    users_db[user_id] = User.from_create(id=user_id, user=user)
    return users_db[user_id]


@router.delete("/{user_id}")
async def delete_user(user_id: int) -> JSONResponse:
    if user_id not in users_db:
        raise UserNotFound()

    del users_db[user_id]
    return JSONResponse(status_code=200, content={"message": f"User {user_id} deleted"})
