# ============================================================
# FastAPI Todo Application – Tutorial Edition
# ============================================================
# This file wires together the app, routes, and dependencies.
# In future chapters, these routes will be split into separate
# modules (auth, todos, errors, etc.).
# ============================================================

# ---- Standard library ----
from typing import List
from pydantic import BaseModel

# ---- Third-party packages ----
from fastapi import FastAPI, HTTPException, Depends

# ---- Local application imports ----
from .models import TodoItem, TodoCreate
from .auth_service import (
    get_current_user,
    authenticate_basic,
)
from .logging_config import setup_logging
from .logging_middleware import register_request_logger
from .db import TodoDB
from .error_handlers import register_error_handlers, APIError

# ---- Routers ----
from app.auth.router import router as auth_router

# ---- Constants ----
from .constants import TODO_NOT_FOUND

# ---- logging setup (moved) ----
setup_logging()

# ---- app ----
app = FastAPI(title="FastAPI Todo Application – Tutorial Edition")
register_request_logger(app)
register_error_handlers(app)
app.include_router(auth_router)

# ---- DB -----
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
