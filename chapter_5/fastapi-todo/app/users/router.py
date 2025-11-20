# ============================================================
# FastAPI routes
# ============================================================
from typing import List

# ---- Third-party packages ----
from fastapi import Depends, APIRouter

from app.users.service import UserService, get_user_service
from app.users.schemas import User
from app.auth.dependencies import require_admin

# ---- Router -----
router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("", response_model=List[User], dependencies=[Depends(require_admin)])
def list_users(
        user_service: UserService = Depends(get_user_service),
):
    """List all users from the database."""
    fetched_users = user_service.list_users()
    return fetched_users