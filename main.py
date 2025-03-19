from fastapi import FastAPI

from lottery.routers import router as lottery_router
from rewards.exceptions import (
    RewardNotFound,
    RewardOverlapException,
    reward_not_found_handler,
    reward_overlap_handler,
)
from rewards.routers import router as rewards_router
from users.exceptions import UserNotFound, user_not_found_handler
from users.routers import router as user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(rewards_router)
app.include_router(lottery_router)


app.add_exception_handler(UserNotFound, user_not_found_handler)
app.add_exception_handler(RewardNotFound, reward_not_found_handler)
app.add_exception_handler(RewardOverlapException, reward_overlap_handler)
