from fastapi import HTTPException, APIRouter, Query, Depends
from rewards.models import Reward, RewardCreate
from typing import Dict


rewards_db: Dict[int, Reward] = {}
reward_id_counter = 0

router = APIRouter(prefix="/rewards", tags=["Rewards"])


def pagination(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    return {"skip": skip, "limit": limit}

@router.get("/")
def get_rewards(pagination: dict = Depends(pagination)):
    skip, limit = pagination["skip"], pagination["limit"]
    return list(rewards_db.values())[skip:skip+limit]

@router.post("/")
def create_reward(reward: RewardCreate):
    for db_reward in rewards_db.values():
        if not (reward.age_to < db_reward.age_from or reward.age_from >= db_reward.age_to):
            raise HTTPException(status_code=400, detail="Overlapping age range with existing reward")
        
    global reward_id_counter
    new_reward = Reward.from_create(id=reward_id_counter, reward=reward)
    rewards_db[reward_id_counter] = new_reward
    reward_id_counter += 1
    return new_reward

@router.put("/{reward_id}")
def update_user(reward_id: int, reward: RewardCreate):
    if reward_id not in rewards_db:
        raise HTTPException(status_code=404, detail="Reward not found")
    
    for db_reward in rewards_db.values():
        if not (reward.age_to < db_reward.age_from or reward.age_from > db_reward.age_to):
            raise HTTPException(status_code=400, detail="Overlapping age range with existing reward")
        
    rewards_db[reward_id] = Reward.from_create(id=reward_id, reward=reward)
    return rewards_db[reward_id]


@router.delete("/{reward_id}")
def create_reward(reward_id: int):
    if reward_id not in rewards_db:
        raise HTTPException(status_code=404, detail="Reward not found")
    
    del rewards_db[reward_id]
    return {"message": f"Reward {reward_id} deleted"}