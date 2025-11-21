# ============================================================
# Core DB connection
# ============================================================
from typing import List
from app.core.security import get_password_hash
from app.users.entities import UserEntity

class DB:
    """
    Database class. Each attribute represents one table in the database.
    At this point this is an append only database.
    """
    def __init__(self, users: List[dict] = None, todos: List[dict] = None):
        self.users = users or []
        self.todos = todos or []




fake_users = [
    UserEntity(
        id=1,
        username="alice",
        hashed_password=get_password_hash("wonderland"),
        name="Alice Sharpe",
        email="asharpe@example.com",
        role="user",
        scopes=["read", "write"],
        disabled=False,
    ),
    UserEntity(
        id=2,
        username="admin",
        hashed_password=get_password_hash("secret"),
        name="Admin",
        email="admin@example.com",
        role="admin",
        scopes=["read", "write", "admin"],
        disabled=False,
    ),
]
fake_todos = []

# Mock database instance
mock_db = DB(fake_users, fake_todos)

def get_db() -> DB:
    return mock_db
