# ============================================================
# Business logic
# ============================================================
from typing import Optional, Iterable, List

from app.core.db import get_db
from app.users.entities import UserEntity
from app.users.repository import UserRepository
from app.core.security import get_password_hash


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(
            self,
            username: str,
            password: str,
            name: Optional[str] = "",
            email: Optional[str] = "",
            scopes: Optional[List[str]] = None,
    ) -> UserEntity:
        hashed_password = get_password_hash(password)
        # Could have business rules here: check domain, etc.
        return self.repo.create_user(
            username=username,
            hashed_password=hashed_password,
            name=name,
            email=email,
            scopes=scopes,
        )

    def get_user(self, username: str) -> Optional[UserEntity]:
        return self.repo.get_user(username)

    def list_users(self) -> Iterable[UserEntity]:
        return self.repo.list_users()


# Create a repo singleton
db = get_db()
user_repo = UserRepository(db)

def get_user_service() -> UserService:
    return UserService(user_repo)
