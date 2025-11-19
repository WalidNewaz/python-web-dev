# ============================================================
# Core DB connection
# ============================================================
from typing import List
from .security import get_password_hash


class DB:
    """
    Database class. Each attribute represents one table in the database.
    At this point this is an append only database.
    """
    def __init__(self, users: List[dict] = None, todos: List[dict] = None):
        self.users = users or []
        self.todos = todos or []


fake_users = [
    {
        "id": 1,
        "username": "alice",
        "hashed_password": get_password_hash("wonderland"),
        "name": "Alice Sharpe",
        "email": "asharpe@example.com",
        "role": "user",
        "scopes": ["read", "write"],
        "disabled": False,
    },
    {
        "id": 2,
        "username": "admin",
        "hashed_password": get_password_hash("secret"),
        "name": "Admin",
        "email": "admin@example.com",
        "role": "admin",
        "scopes": ["read", "write", "admin"],
        "disabled": False,
    }
]
fake_todos = []

# Mock database instance
mock_db = DB(fake_users, fake_todos)

def get_db() -> DB:
    return mock_db
