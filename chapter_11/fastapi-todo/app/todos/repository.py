# ============================================================
# DB access layer
# ============================================================
from typing import Protocol, Iterable
from sqlalchemy.orm import Session

from app.todos.models import TodoBaseModel


class TodoRepositoryProtocol(Protocol):
    def list_todos(self) -> Iterable[TodoBaseModel ]: ...

    def create_todo(self, title: str, completed: bool) -> TodoBaseModel : ...

    def get_todo(self, id: int) -> TodoBaseModel : ...

    def update_todo(self, id: int, title: str, completed: bool) -> TodoBaseModel : ...

    def delete_todo(self, id: int) -> TodoBaseModel : ...


class TodoRepository(TodoRepositoryProtocol):
    def __init__(self, db: Session):
        self.db = db

    def list_todos(self):
        """Return all todos."""
        return self.db.query(TodoBaseModel).all()

    def create_todo(self, title: str, completed: bool) -> TodoBaseModel :
        """Adds a new TodoItem to the database."""
        new_todo = TodoBaseModel (title=title, completed=completed)
        self.db.add(new_todo)
        self.db.commit()
        self.db.refresh(new_todo)
        return new_todo

    def get_todo(self, id: int):
        """Retrieve a Todo item by ID."""
        found_todo = self.db.get(TodoBaseModel, id)
        return found_todo

    def update_todo(self, id: int, title: str, completed: bool) -> TodoBaseModel :
        """Update a Todo item by ID."""
        found_todo = self.get_todo(id)
        if found_todo is None:
            return None
        found_todo.title = title
        found_todo.completed = completed
        self.db.add(found_todo)
        self.db.commit()
        self.db.refresh(found_todo)
        return found_todo

    def delete_todo(self, id: int) -> TodoBaseModel :
        """Deletes an item by ID."""
        found_todo = self.get_todo(id)
        if found_todo is None:
            return None
        self.db.delete(found_todo)
        self.db.commit()
        return found_todo
