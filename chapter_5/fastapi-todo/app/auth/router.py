# ============================================================
# FastAPI routes
# ============================================================

# ---- Standard library ----
from datetime import timedelta

# ---- Third-party packages ----
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

# ---- Local application imports ----
from app.models import Token, User
from app.auth_service import (
    create_token,
    verify_password,
    create_access_token_from_refresh,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)
from app.db import UserDB

# ---- Router -----
router = APIRouter(prefix="/auth", tags=["auth"])

# ---- DB -----
users = UserDB()

@router.post("/token", response_model=Token, response_model_exclude_none=True)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token."""
    fetched_user = users.get_user(username=form_data.username)
    if not fetched_user or not verify_password(form_data.password, fetched_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    user = User(**{k: fetched_user[k] for k in ("username", "role", "scopes", "name", "email")})
    access_token = create_token(
        {"sub": user.username, "scopes": user.scopes},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {"sub": user.username, "scopes": user.scopes, "type": "refresh"},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token": refresh_token,
        "info": {
            "name": user.name,
            "email": user.email,
        }
    }

@router.post("/refresh", response_model=Token, response_model_exclude_none=True)
def refresh_token_endpoint(refresh_token: str):
    access_token = create_access_token_from_refresh(refresh_token)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }