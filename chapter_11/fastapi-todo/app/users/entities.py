# ============================================================
# Business/domain entities
# ============================================================
from dataclasses import dataclass
from typing import List


@dataclass
class UserEntity:
    id: int
    username: str
    hashed_password: str
    name: str
    email: str
    role: str
    scopes: List[str]
    disabled: bool