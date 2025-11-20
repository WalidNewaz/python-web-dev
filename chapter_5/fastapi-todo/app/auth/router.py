# ============================================================
# FastAPI routes
# ============================================================

# ---- Standard library ----
from datetime import timedelta

# ---- Third-party packages ----
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

# ---- Local application imports ----
from app.auth.schemas import Token
from app.users.schemas import User, UserRegisterSchema, UserRegOutSchema
from app.users.service import UserService, get_user_service
from app.auth.service import (
    AuthService,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)
from app.auth.dependencies import get_auth_service

# ---- Router -----
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token", response_model=Token, response_model_exclude_none=True)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(get_user_service),
        auth_service: AuthService = Depends(get_auth_service)
):
    """Authenticate user and return JWT token."""
    fetched_user = user_service.get_user(form_data.username)
    if not fetched_user or not auth_service.verify_password(form_data.password, fetched_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    user = User(
        id=fetched_user.id,
        username=fetched_user.username,
        disabled=fetched_user.disabled,
        role=fetched_user.role,
        name=fetched_user.name,
        email=fetched_user.email,
        scopes=fetched_user.scopes,
    )
    access_token = auth_service.create_token(
        {"sub": user.username, "scopes": user.scopes, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = auth_service.create_token(
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
def refresh_token_endpoint(
        refresh_token: str,
        auth_service: AuthService = Depends(get_auth_service)
):
    access_token = auth_service.create_access_token_from_refresh(refresh_token)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }

@router.post("/register", response_model=UserRegOutSchema, response_model_exclude_none=True)
def register_user(
        user_register: UserRegisterSchema,
        user_service: UserService = Depends(get_user_service),
):
    """Register a new user."""
    fetched_user = user_service.get_user(user_register.username)
    if fetched_user:
        raise HTTPException(status_code=400, detail="User already exists")

    created_user = user_service.register_user(
        username=user_register.username,
        password=user_register.password,
        name=user_register.name,
        email=user_register.email,
        scopes=["read", "write"]

    )
    return created_user

