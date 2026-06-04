"""In-memory пользователи (задания 11.1 и 11.2)."""

from itertools import count
from threading import Lock

from fastapi import APIRouter, HTTPException, Response, status

from app.schemas import User, UserIn, UserOut

router = APIRouter(tags=["users"])

# In-memory "БД".
db: dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()


def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    user_id = next_user_id()
    db[user_id] = user.model_dump()
    return {"id": user_id, **db[user_id]}


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db[user_id]}


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if db.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Эндпоинт со строгой валидацией (задание 11.1).
@router.post("/users/validate", status_code=201)
def validate_user(user: User):
    return {"status": "ok", "user": user.model_dump()}
