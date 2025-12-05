# ============================================================
# Database models
# ============================================================
from sqlalchemy import Column, Integer, String, Boolean
from app.core.db import Base

class UsersBaseModel(Base):
    """SQLAlchemy model for users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    name = Column(String)
    email = Column(String)
    role = Column(String)
    scopes = Column(String)
    disabled = Column(Boolean, default=False)

