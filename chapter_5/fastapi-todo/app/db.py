from typing import List
from .models import TodoItem, User
# from .auth_service import get_password_hash

# In-memory Todo list
todos: List[TodoItem] = []
next_id: int = 1

class TodoDB:
    def __init__(self):
        self.todos: List[TodoItem] = []
        self.next_id: int = 1

    def get_all_todos(self) -> List[TodoItem]:
        """Fetch all todos."""
        return self.todos

    def get_todo(self, todo_id: int) -> TodoItem:
        """Fetches a TodoItem by ID."""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo

        return None

    def add_item(self, title: str, completed: bool) -> TodoItem:
        """Adds a new TodoItem to the database."""
        new_todo = TodoItem(id=self.next_id, title=title, completed=completed)
        self.todos.append(new_todo)
        self.next_id += 1
        return new_todo

    def update_item(self, todo_id: int, title: str, completed: bool) -> TodoItem:
        """Update a TodoItem by ID."""
        for todo in self.todos:
            if todo.id == todo_id:
                todo.title = title
                todo.completed = completed
                return todo

        return None

    def delete_item(self, todo_id: int) -> TodoItem:
        """Deletes an item by ID."""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                deleted_todo = self.todos.pop(i)
                return deleted_todo

        return None

