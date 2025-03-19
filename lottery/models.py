from typing import List

from pydantic import BaseModel


class LoterryWinner(BaseModel):
    name: str
    reward: str


class LotteryResult(BaseModel):
    winner_list: List[LoterryWinner]
