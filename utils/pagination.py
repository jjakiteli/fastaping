from fastapi import Query


def pagination(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)) -> dict:
    return {"skip": skip, "limit": limit}
