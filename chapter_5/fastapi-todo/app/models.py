from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TodoItem(BaseModel):
    """Represents a Todo item."""
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    completed: bool = False

class TodoCreate(BaseModel):
    """Model for creating a new Todo item."""
    title: str = Field(..., min_length=1, max_length=100)
    completed: Optional[bool] = False

# class Token(BaseModel):
#     access_token: str
#     token_type: str
#     expires_in: Optional[datetime] = None
#     refresh_token: Optional[str] = None
#     scope: Optional[str] = None
#     uid: Optional[str] = None
#     info: Optional[dict] = None


class User(BaseModel):
    username: str
    disabled: bool = False
    hashed_password: Optional[str] = None
    role: str
    name: str
    email: str
    scopes: List[str]