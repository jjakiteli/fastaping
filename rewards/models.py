from pydantic import BaseModel


class RewardCreate(BaseModel):
    name: str
    age_from: int
    age_to: int
    
class Reward(BaseModel):
    id: int
    name: str
    age_from: int
    age_to: int
    
    @classmethod
    def from_create(cls, id: int, reward: RewardCreate):
        return cls(
            id=id,
            name=reward.name,
            age_from=reward.age_from,
            age_to=reward.age_to
        )