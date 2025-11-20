# ============================================================
# DB access layer
# ============================================================
from typing import Protocol, Optional, Iterable, List
from app.users.entities import UserEntity
from app.core.db import DB


class UserRepositoryProtocol(Protocol):
    def create_user(
            self,
            username: str,
            hashed_password: str,
            name: str,
            email: str,
            scopes: List[str],
    ) -> UserEntity: ...

    def get_user(self, username: str) -> Optional[UserEntity]: ...

    def list_users(self) -> Iterable[UserEntity]: ...


class UserRepository(UserRepositoryProtocol):
    def __init__(self, db: DB):
        self.db = db

    def create_user(
            self,
            username: str,
            hashed_password: str,
            name: str,
            email: str,
            scopes: List[str],
    ) -> UserEntity:
        """Adds a new user to the database."""
        user = UserEntity(
            id=len(self.db.users) + 1,
            username=username,
            hashed_password=hashed_password,
            name=name,
            email=email,
            scopes=scopes,
            role="user",
            disabled=False
        )
        self.db.users.append(user)
        return user

    def get_user(self, username: str) -> Optional[UserEntity]:
        """Returns the user found in the users list."""
        found_user = next((user for user in self.db.users if user.username == username), None)
        return found_user

    def list_users(self) -> Iterable[UserEntity]:
        """Returns the users list."""
        return self.db.users
