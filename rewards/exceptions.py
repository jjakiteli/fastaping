from fastapi import Request
from fastapi.responses import JSONResponse


class RewardNotFound(Exception):
    def __init__(self, message: str = "Reward not found"):
        self.message = message
        self.status_code = 404
        super().__init__(message)


async def reward_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RewardNotFound):
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


class RewardOverlapException(Exception):
    def __init__(self, message: str = "Overlapping age range with existing reward"):
        self.message = message
        self.status_code = 400
        super().__init__(message)


async def reward_overlap_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RewardOverlapException):
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
