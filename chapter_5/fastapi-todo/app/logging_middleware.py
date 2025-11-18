import time
import logging
from typing import Callable, Awaitable
from fastapi import FastAPI, Request
from starlette.responses import Response

async def request_logger(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Middleware function that logs method, path, and duration."""
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logging.info(f"{request.method} {request.url.path} completed in {duration:.4f}s")
    return response

def register_request_logger(app: FastAPI) -> None:
    """Registers the request_logger as an HTTP middleware on the given app."""
    @app.middleware("http")
    async def _mw(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        return await request_logger(request, call_next)