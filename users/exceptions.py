from fastapi import Request
from fastapi.responses import JSONResponse


class UserNotFound(Exception):
    def __init__(self, message: str = "User not found"):
        self.message = message
        self.status_code = 404
        super().__init__(message)


async def user_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, UserNotFound):
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
