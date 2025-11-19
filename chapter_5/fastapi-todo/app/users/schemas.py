# ============================================================
# Pydantic request/response models
# ============================================================
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    disabled: bool = False
    hashed_password: Optional[str] = None
    role: str
    name: str
    email: str
    scopes: List[str]