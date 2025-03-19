from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    age: int
    role: str


class User(BaseModel):
    id: int
    name: str
    age: int
    role: str

    @classmethod
    def from_create(cls, id: int, user: UserCreate):
        return cls(id=id, name=user.name, age=user.age, role=user.role)
