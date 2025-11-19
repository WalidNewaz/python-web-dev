# ============================================================
# Pydantic request/response models
# ============================================================
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: Optional[datetime] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    uid: Optional[str] = None
    info: Optional[dict] = None