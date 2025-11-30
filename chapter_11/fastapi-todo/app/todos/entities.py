# ============================================================
# Business/domain entities
# ============================================================
from dataclasses import dataclass

@dataclass
class TodoItemEntity:
    id: int = None
    title: str = None
    completed: bool = False