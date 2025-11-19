# ============================================================
# FastAPI routes
# ============================================================
from typing import List

# ---- Third-party packages ----
from fastapi import Depends, APIRouter, HTTPException

from app.core.db import get_db
from app.auth.service import (
    AuthService,
)
from app.todos.repository import TodoRepository
from app.todos.service import TodoService
from app.todos.schemas import TodoItem, TodoCreate

# ---- Constants ----
from app.constants import TODO_NOT_FOUND

# ---- Router -----
router = APIRouter(prefix="/api/todos", tags=["ToDos"])


def get_todo_service(db=Depends(get_db)) -> TodoService:
    repo = TodoRepository(db)
    return TodoService(repo)



@router.get("", dependencies=[Depends(AuthService.get_current_user)])
def list_todos(
        todo_service: TodoService = Depends(get_todo_service),
) -> List[TodoItem]:
    """List todos, but only if API key is valid."""
    return todo_service.list_todos()


@router.post("", dependencies=[Depends(AuthService.get_current_user)])
def create_todo(
        todo: TodoCreate,
        todo_service: TodoService = Depends(get_todo_service),
) -> TodoItem:
    """Create a new Todo item."""
    return todo_service.create_todo(title=todo.title, completed=False)


@router.get("/{todo_id}", dependencies=[Depends(AuthService.get_current_user)])
def get_todo(todo_id: int, todo_service: TodoService = Depends(get_todo_service)) -> TodoItem:
    """Retrieve a Todo item by ID."""
    todo = todo_service.get_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo

@router.put("/{todo_id}", dependencies=[Depends(AuthService.get_current_user)])
def update_todo(
        todo_id: int,
        updated_todo: TodoCreate,
        todo_service: TodoService = Depends(get_todo_service)
) -> TodoItem:
    """Update a Todo item by ID."""
    todo = todo_service.update_todo(todo_id, updated_todo.title, updated_todo.completed)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo

@router.delete("/{todo_id}", dependencies=[Depends(AuthService.get_current_user)])
def delete_todo(todo_id: int, todo_service: TodoService = Depends(get_todo_service)):
    """Delete a Todo item by ID."""
    todo = todo_service.delete_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo