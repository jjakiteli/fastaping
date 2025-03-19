from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from rewards.models import Reward, RewardCreate
from utils.pagination import pagination

rewards_db: Dict[int, Reward] = {}
reward_id_counter = 0

router = APIRouter(prefix="/rewards", tags=["Rewards"])


@router.get("/")
async def get_rewards(
    pagination: Annotated[Dict[str, int], Depends(pagination)],
) -> List[Reward]:
    skip, limit = pagination["skip"], pagination["limit"]
    return list(rewards_db.values())[skip : skip + limit]


@router.post("/")
async def create_reward(reward: RewardCreate) -> Reward:
    for db_reward in rewards_db.values():
        if not (
            reward.age_to < db_reward.age_from or reward.age_from >= db_reward.age_to
        ):
            raise HTTPException(
                status_code=400, detail="Overlapping age range with existing reward"
            )

    global reward_id_counter
    new_reward = Reward.from_create(id=reward_id_counter, reward=reward)
    rewards_db[reward_id_counter] = new_reward
    reward_id_counter += 1
    return new_reward


@router.put("/{reward_id}")
async def update_user(reward_id: int, reward: RewardCreate) -> Reward:
    if reward_id not in rewards_db:
        raise HTTPException(status_code=404, detail="Reward not found")

    for db_reward in rewards_db.values():
        if not (
            reward.age_to < db_reward.age_from or reward.age_from > db_reward.age_to
        ):
            raise HTTPException(
                status_code=400, detail="Overlapping age range with existing reward"
            )

    rewards_db[reward_id] = Reward.from_create(id=reward_id, reward=reward)
    return rewards_db[reward_id]


@router.delete("/{reward_id}")
async def delete_reward(reward_id: int) -> JSONResponse:
    if reward_id not in rewards_db:
        raise HTTPException(status_code=404, detail="Reward not found")

    del rewards_db[reward_id]
    return JSONResponse(
        status_code=200, content={"message": f"Reward {reward_id} deleted"}
    )
