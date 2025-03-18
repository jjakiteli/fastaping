from fastapi import HTTPException, APIRouter, Query, Depends
from users.models import User, UserCreate
from typing import Dict


users_db: Dict[int, User] = {}
user_id_counter = 0

router = APIRouter(prefix="/users", tags=["Users"])


def pagination(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    return {"skip": skip, "limit": limit}

@router.get("/")
def get_users(pagination: dict = Depends(pagination)):
    skip, limit = pagination["skip"], pagination["limit"]
    return list(users_db.values())[skip:skip+limit]

@router.post("/")
def create_user(user: UserCreate):
    global user_id_counter
    new_user = User.from_create(id=user_id_counter, user=user)
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user

@router.put("/{user_id}")
def update_user(user_id: int, user: UserCreate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db[user_id] = User.from_create(id=user_id, user=user)
    return users_db[user_id]