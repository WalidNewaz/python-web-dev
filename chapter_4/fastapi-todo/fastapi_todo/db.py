from typing import List
from .models import TodoItem
from .auth_service import get_password_hash

# In-memory Todo list
todos: List[TodoItem] = []
next_id: int = 1

# Simple user store
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": get_password_hash("wonderland"),
    }
}
