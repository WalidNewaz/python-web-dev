# ============================================================
# DB access layer
# ============================================================
from typing import Protocol, Iterable

from app.todos.entities import TodoItemEntity
from app.core.db import DB


class TodoRepositoryProtocol(Protocol):
    def list_todos(self) -> Iterable[TodoItemEntity]: ...

    def create_todo(self, title: str, completed: bool) -> TodoItemEntity: ...

    def get_todo(self, id: int) -> TodoItemEntity: ...

    def update_todo(self, id: int, title: str, completed: bool) -> TodoItemEntity: ...

    def delete_todo(self, id: int) -> TodoItemEntity: ...


class TodoRepository(TodoRepositoryProtocol):
    def __init__(self, db: DB):
        self.db = db

    def list_todos(self):
        """Return all todos."""
        return self.db.todos

    def create_todo(self, title: str, completed: bool) -> TodoItemEntity:
        """Adds a new TodoItem to the database."""
        new_todo = TodoItemEntity(
            id=len(self.db.todos) + 1,
            title=title,
            completed=completed
        )
        self.db.todos.append(new_todo)
        return new_todo

    def get_todo(self, id: int):
        """Retrieve a Todo item by ID."""
        found = next((todo for todo in self.db.todos if todo.id == id), None)
        return found

    def update_todo(self, id: int, title: str, completed: bool) -> TodoItemEntity:
        """Update a Todo item by ID."""
        for todo in self.db.todos:
            if todo.id == id:
                todo.title = title
                todo.completed = completed
                return todo

        return None

    def delete_todo(self, id: int) -> TodoItemEntity:
        """Deletes an item by ID."""
        for i, todo in enumerate(self.db.todos):
            if todo.id == id:
                deleted_todo = self.db.todos.pop(i)
                return deleted_todo

        return None

