from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError


# ---------------------------
# Custom exception class
# ---------------------------
class APIError(Exception):
    """Custom application-level error."""
    def __init__(self, code: int, message: str, details: dict | None = None):
        self.code = code
        self.message = message
        self.details = details or {}


# ---------------------------
# Handlers
# ---------------------------
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom handler for FastAPI validation errors."""
    return JSONResponse(
        status_code=422,
        content={"error": "Validation failed", "details": exc.errors()},
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom handler for general FastAPI HTTPException."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


async def api_error_handler(request: Request, exc: APIError):
    """Custom handler for our own APIError."""
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.message, "details": exc.details},
    )


# ---------------------------
# Registration helper
# ---------------------------
def register_error_handlers(app):
    """Attach all handlers to a FastAPI app."""
    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.exception_handler(HTTPException)(http_exception_handler)
    app.exception_handler(APIError)(api_error_handler)
