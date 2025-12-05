# ============================================================
# Database models
# ============================================================

from sqlalchemy import Column, Integer, String, Boolean
from app.core.db import Base

class TodoBaseModel(Base):
    """SQLAlchemy model for todos."""

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)