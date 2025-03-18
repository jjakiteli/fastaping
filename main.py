from fastapi import FastAPI

from users.routers import router as user_router
from rewards.routers import router as rewards_router
from lottery.routers import router as lottery_router


app = FastAPI()
app.include_router(user_router)
app.include_router(rewards_router)
app.include_router(lottery_router)

