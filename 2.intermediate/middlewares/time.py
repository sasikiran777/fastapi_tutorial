import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Depends


class TimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_timer = time.time()
        response = await call_next(request)
        process_time = time.time() - start_timer
        response.headers["X-Process-Time"] = f"{process_time:.2f}"
        return response
