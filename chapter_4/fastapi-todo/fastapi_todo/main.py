# ============================================================
# 🚀 FastAPI Todo Application – Tutorial Edition
# ============================================================
# This file wires together the app, routes, and dependencies.
# In future chapters, these routes will be split into separate
# modules (auth, todos, errors, etc.).
# ============================================================

# ---- Standard library ----
from typing import List

# ---- Third-party packages ----
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

# ---- Local application imports ----
from .models import TodoItem, TodoCreate
from .auth_service import (
    create_access_token,
    verify_password,
    get_current_user,
    authenticate_basic,
)
from .logging_config import setup_logging
from .logging_middleware import register_request_logger
from . import db
from .error_handlers import register_error_handlers, APIError

# ---- Constants ----
from .constants import TODO_NOT_FOUND

# ---- logging setup (moved) ----
setup_logging()

# ---- app ----
app = FastAPI()
register_request_logger(app)
register_error_handlers(app)


# ---- Todo CRUD Routes ----

@app.post("/todos", response_model=TodoItem, status_code=201)
def create_todo(todo: TodoCreate) -> TodoItem:
    """Create a new Todo item."""
    new_todo = TodoItem(id=db.next_id, title=todo.title, completed=False)
    db.todos.append(new_todo)
    db.next_id += 1
    return new_todo


@app.get("/todos", response_model=List[TodoItem])
def list_todos() -> List[TodoItem]:
    """List all Todo items."""
    return db.todos


@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int) -> TodoItem:
    """Retrieve a Todo item by ID."""
    for todo in db.todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)


@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoCreate) -> TodoItem:
    """Update a Todo item by ID."""
    for todo in db.todos:
        if todo.id == todo_id:
            todo.title = updated_todo.title
            return todo
    raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)


@app.delete("/todos/{todo_id}", response_model=TodoItem)
def delete_todo(todo_id: int) -> TodoItem:
    """Delete a Todo item by ID."""
    for i, todo in enumerate(db.todos):
        if todo.id == todo_id:
            deleted_todo = db.todos.pop(i)
            return deleted_todo
    raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)

# ---- Auth Routes ----

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """Authenticate user and return JWT token."""
    user = db.fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/secure-todos", dependencies=[Depends(get_current_user)])
def secure_list_todos() -> List[TodoItem]:
    """List todos, but only if API key is valid."""
    return db.todos

@app.get("/profile")
def read_profile(username: str = Depends(authenticate_basic)):
    return {"message": f"Hello, {username}!"}

# ---- Utility Routes ----

@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise APIError(
            code=400,
            message="Division by zero is not allowed",
            details={"a": a, "b": b}
        )
    return {"result": a / b}


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint returning a welcome message.
    :return:
        dict[str, str]: JSON response with a message.
    """
    return {"message": "Welcome to FastAPI!"}
