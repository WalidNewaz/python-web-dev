# ============================================================
# Business logic
# ============================================================
from typing import Optional, Iterable
from app.users.entities import UserEntity
from app.users.repository import UserRepositoryProtocol
from app.core.security import get_password_hash


class UserService:
    def __init__(self, repo: UserRepositoryProtocol):
        self.repo = repo

    def register_user(self, username: str, password: str) -> UserEntity:
        # TODO: inject real hasher; this is just tutorial-level
        hashed_password = get_password_hash(password)
        # Could have business rules here: check domain, etc.
        return self.repo.create_user(username=username, hashed_password=hashed_password)

    def get_user(self, username: str) -> Optional[UserEntity]:
        return self.repo.get_user(username)

    def list_users(self) -> Iterable[UserEntity]:
        return self.repo.list_users()



