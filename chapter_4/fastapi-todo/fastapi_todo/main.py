# ============================================================
# 🚀 FastAPI Todo Application – Tutorial Edition
# ============================================================
# This file wires together the app, routes, and dependencies.
# In future chapters, these routes will be split into separate
# modules (auth, todos, errors, etc.).
# ============================================================

# ---- Standard library ----
from typing import List
from datetime import timedelta
from pydantic import BaseModel

# ---- Third-party packages ----
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

# ---- Local application imports ----
from .models import TodoItem, TodoCreate, Token, User
from .auth_service import (
    create_token,
    get_current_user,
    verify_password,
    authenticate_basic,
    create_access_token_from_refresh,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)
from .logging_config import setup_logging
from .logging_middleware import register_request_logger
from .db import UserDB, TodoDB
from .error_handlers import register_error_handlers, APIError

# ---- Constants ----
from .constants import TODO_NOT_FOUND

# ---- logging setup (moved) ----
setup_logging()

# ---- app ----
app = FastAPI()
register_request_logger(app)
register_error_handlers(app)

# ---- DB -----
users = UserDB()
todos = TodoDB()

# ---- Todo CRUD Routes ----

@app.post("/todos", response_model=TodoItem, status_code=201)
def create_todo(todo: TodoCreate) -> TodoItem:
    """Create a new Todo item."""
    new_todo = todos.add_item(title=todo.title, completed=False)
    return new_todo


@app.get("/todos", response_model=List[TodoItem])
def list_todos() -> List[TodoItem]:
    """List all Todo items."""
    return todos.get_all_todos()


@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int) -> TodoItem:
    """Retrieve a Todo item by ID."""
    todo = todos.get_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo


@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoCreate) -> TodoItem:
    """Update a Todo item by ID."""
    todo = todos.update_item(todo_id, updated_todo.title, updated_todo.completed)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo


@app.delete("/todos/{todo_id}", response_model=TodoItem)
def delete_todo(todo_id: int) -> TodoItem:
    """Delete a Todo item by ID."""
    todo = todos.delete_item(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo

# ---- Todo Secure CRUD Routes ----

@app.get("/api/todos", dependencies=[Depends(get_current_user)])
def secure_list_todos() -> List[TodoItem]:
    """List todos, but only if API key is valid."""
    return todos.get_all_todos()

# ---- Auth Routes ----

@app.post("/auth/token", response_model=Token, response_model_exclude_none=True)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token."""
    fetched_user = users.get_user(username=form_data.username)
    if not fetched_user or not verify_password(form_data.password, fetched_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = User(**{k: fetched_user[k] for k in ("username", "role", "scopes", "name", "email")})
    access_token = create_token(
        {"sub": user.username, "scopes": user.scopes},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {"sub": user.username, "scopes": user.scopes, "type": "refresh"},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token": refresh_token,
        "info": {
            "name": user.name,
            "email": user.email,
        }
    }

@app.post("/auth/refresh", response_model=Token, response_model_exclude_none=True)
def refresh_token_endpoint(refresh_token: str):
    access_token = create_access_token_from_refresh(refresh_token)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


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
