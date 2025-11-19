# ============================================================
# Pydantic request/response models
# ============================================================
from pydantic import BaseModel, Field

class TodoItem(BaseModel):
    """Represents a Todo item."""
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    completed: bool = False