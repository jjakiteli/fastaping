from fastapi import HTTPException, APIRouter
from users.routers import users_db
from rewards.routers import rewards_db
import random


router = APIRouter(prefix="/lottery", tags=["Lottery"])

@router.get("/")
def lottery(num_winners: int, default_award: str):
    users = list(users_db.values())
    if len(users) < num_winners:
        raise HTTPException(status_code=400, detail="Not enough users for this lottery")
    
    rewards = list(rewards_db.values())
    winners = random.sample(users, num_winners)
    
    return_list = []
    for winner in winners:
        for db_reward in rewards:
            if winner.age >= db_reward.age_from and winner.age < db_reward.age_to:
                return_list.append({"user": winner, "reward": db_reward.name})
                break
        else:
            return_list.append({"user": winner, "reward": default_award})
            
    return return_list