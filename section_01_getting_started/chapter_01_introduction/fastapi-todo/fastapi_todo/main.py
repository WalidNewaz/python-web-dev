import time
import logging
from typing import List

from fastapi import FastAPI, HTTPException, Request, Depends
from .models import TodoItem, TodoCreate
from .dependencies import get_api_key

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Setup app
app = FastAPI()

# In-memory store
todos: List[TodoItem] = []
next_id = 1

@app.middleware("http")
async def log_request(request: Request, call_next):
    """Middleware to log request method, path, and execution time."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logging.info(f"{request.method} {request.url.path} completed in {duration:.4f}s")
    return response

@app.post("/todos", response_model=TodoItem, status_code=201)
def create_todo(todo: TodoCreate) -> TodoItem:
    """Create a new Todo item."""
    global next_id
    new_todo = TodoItem(id=next_id, title=todo.title, completed=False)
    todos.append(new_todo)
    next_id += 1
    return new_todo

@app.get("/todos", response_model=List[TodoItem])
def list_todos() -> List[TodoItem]:
    """List all Todo items."""
    return todos

@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int) -> TodoItem:
    """Retrieve a Todo item by ID."""
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo item not found")

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoCreate) -> TodoItem:
    """Update a Todo item by ID."""
    for todo in todos:
        if todo.id == todo_id:
            todo.title = updated_todo.title
            return todo
    raise HTTPException(status_code=404, detail="Todo item not found")

@app.delete("/todos/{todo_id}", response_model=TodoItem)
def delete_todo(todo_id: int) -> TodoItem:
    """Delete a Todo item by ID."""
    global todos
    deleted_todo = next((todo for todo in todos if todo.id == todo_id), None)
    if deleted_todo:
        todos = [todo for todo in todos if todo.id != todo_id]
        return deleted_todo
    raise HTTPException(status_code=404, detail="Todo item not found")

@app.get("/secure-todos", dependencies=[Depends(get_api_key)])
def secure_list_todos() -> List[TodoItem]:
    """List todos, but only if API key is valid."""
    return todos


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint returning a welcome message.

    :return:
        dict[str, str]: JSON response with a message.
    """
    return {"message": "Welcome to FastAPI!"}