from typing import List

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.security import OAuth2PasswordRequestForm

from .models import TodoItem, TodoCreate
from .auth_service import (
    create_access_token,
    verify_password,
    get_current_user,
)
from .logging_config import setup_logging
from .logging_middleware import register_request_logger
from . import db

# ---- logging setup (moved) ----
setup_logging()

# ---- app ----
app = FastAPI()
register_request_logger(app)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    """Custom handler for validation errors."""
    return JSONResponse(
        status_code=422,
        content={"error": "Validation failed", "details": exc.errors()},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc):
    """Custom handler for HTTP errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


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
    raise HTTPException(status_code=404, detail="Todo item not found")

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoCreate) -> TodoItem:
    """Update a Todo item by ID."""
    for todo in db.todos:
        if todo.id == todo_id:
            todo.title = updated_todo.title
            return todo
    raise HTTPException(status_code=404, detail="Todo item not found")

@app.delete("/todos/{todo_id}", response_model=TodoItem)
def delete_todo(todo_id: int) -> TodoItem:
    """Delete a Todo item by ID."""
    deleted_todo = next((todo for todo in db.todos if todo.id == todo_id), None)
    if deleted_todo:
        db.todos = [todo for todo in db.todos if todo.id != todo_id]
        return deleted_todo
    raise HTTPException(status_code=404, detail="Todo item not found")

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

# Include your APIError and handler here
class APIError(Exception):
    def __init__(self, code: int, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.message, "details": exc.details}
    )

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