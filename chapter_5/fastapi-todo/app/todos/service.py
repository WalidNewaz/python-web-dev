# ============================================================
# Business logic
# ============================================================
from typing import Iterable

from app.todos.entities import TodoItemEntity
from app.todos.repository import TodoRepositoryProtocol

class TodoService:
    def __init__(self, repository: TodoRepositoryProtocol):
        self.repository = repository

    def list_todos(self) -> Iterable[TodoItemEntity]:
        return self.repository.list_todos()

    def create_todo(self, title: str, completed: bool) -> TodoItemEntity:
        return self.repository.create_todo(title=title, completed=completed)

    def get_todo(self, todo_id: int) -> TodoItemEntity:
        return self.repository.get_todo(todo_id)

    def update_todo(self, todo_id: int, title: str, completed: bool) -> TodoItemEntity:
        return self.repository.update_todo(todo_id, title=title, completed=completed)

    def delete_todo(self, todo_id: int) -> TodoItemEntity:
        return self.repository.delete_todo(todo_id)

