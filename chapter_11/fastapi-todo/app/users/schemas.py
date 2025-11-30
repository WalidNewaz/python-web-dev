# ============================================================
# Pydantic request/response models
# ============================================================
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    username: str
    disabled: bool = False
    role: str
    name: str
    email: str
    scopes: List[str]

class UserRegisterSchema(BaseModel):
    username: str
    password: str
    name: str
    email: Optional[EmailStr] = None

class UserRegOutSchema(BaseModel):
    username: str
    name: str
    role: str