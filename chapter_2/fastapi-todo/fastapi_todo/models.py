from pydantic import BaseModel, Field

class TodoItem(BaseModel):
    """Represents a Todo item."""
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    completed: bool = False

class TodoCreate(BaseModel):
    """Model for creating a new Todo item."""
    title: str = Field(..., min_length=1, max_length=100)

