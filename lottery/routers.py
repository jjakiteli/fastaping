import random

from fastapi import APIRouter, HTTPException

from lottery.models import LoterryWinner, LotteryResult
from rewards.routers import rewards_db
from users.routers import users_db

router = APIRouter(prefix="/lottery", tags=["Lottery"])


@router.get("/")
async def run_lottery(num_winners: int, default_award: str) -> LotteryResult:
    users = list(users_db.values())
    if len(users) < num_winners:
        raise HTTPException(status_code=400, detail="Not enough users for this lottery")

    rewards = list(rewards_db.values())
    winners = random.sample(users, num_winners)

    result = LotteryResult(winner_list=[])
    for winner in winners:
        for db_reward in rewards:
            if winner.age >= db_reward.age_from and winner.age < db_reward.age_to:
                result.winner_list.append(
                    LoterryWinner(name=winner.name, reward=db_reward.name)
                )
                break
        else:
            result.winner_list.append(
                LoterryWinner(name=winner.name, reward=default_award)
            )

    return result
