# ============================================================
# FastAPI Todo Application – Tutorial Edition
# ============================================================
# This file wires together the app, routes, and dependencies.
# In future chapters, these routes will be split into separate
# modules (auth, todos, errors, etc.).
# ============================================================

# ---- Standard library ----
from pydantic import BaseModel

# ---- Third-party packages ----
from fastapi import FastAPI, Depends

# ---- Local application imports ----
from app.core.logging_config import setup_logging
from app.core.logging_middleware import register_request_logger
from app.core.error_handlers import register_error_handlers, APIError
from app.auth.dependencies import authenticate_basic

# ---- Routers ----
from app.auth.router import router as auth_router
from app.todos.router import router as todos_router
from app.users.router import router as users_router

# ---- logging setup (moved) ----
setup_logging()

# ---- app ----
app = FastAPI(title="FastAPI Todo Application – Tutorial Edition")
register_request_logger(app)
register_error_handlers(app)

# ---- Auth Routes ----
app.include_router(auth_router)

# ---- Todo CRUD Routes ----
app.include_router(todos_router)

# ---- User Routes -----
app.include_router(users_router)

# ---- Demo Routes ----

class BasicAuthDemoResponse(BaseModel):
    message: str

@app.get("/demo/basic-auth", response_model=BasicAuthDemoResponse)
def read_profile(username: str = Depends(authenticate_basic)):
    """A simple demonstration of the basic auth mechanism."""
    return {"message": f"Hello, {username}!"}

class DivResponse(BaseModel):
    result: float

@app.get("/util/divide", response_model=DivResponse)
def divide(a: float, b: float):
    """A simple utility function that divides two numbers."""
    if b == 0:
        raise APIError(
            code=400,
            message="Division by zero is not allowed",
            details={"a": a, "b": b}
        )
    return {"result": a / b}

# ---- Utility Routes ----

class RootResponse(BaseModel):
    message: str

@app.get("/", response_model=RootResponse)
def root():
    """Root endpoint returning a welcome message.
    :return:
        dict[str, str]: JSON response with a message.
    """
    return {"message": "Welcome to FastAPI!"}
