# ============================================================
# FastAPI routes
# ============================================================

# ---- Standard library ----
from datetime import timedelta

# ---- Third-party packages ----
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

# ---- Local application imports ----
from .schemas import Token
from app.users.schemas import User
from app.core.db import get_db
from app.core.security import get_pwd_ctx
from app.users.repository import UserRepository
from app.users.service import UserService
from .service import AuthService, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

# ---- Router -----
router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service(db=Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


def get_auth_service(pwd_context=Depends(get_pwd_ctx)):
    return AuthService(pwd_context)


@router.post("/token", response_model=Token, response_model_exclude_none=True)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(get_user_service),
        auth_service: AuthService = Depends(get_auth_service)
):
    """Authenticate user and return JWT token."""
    fetched_user = user_service.get_user(form_data.username)
    if not fetched_user or not auth_service.verify_password(form_data.password, fetched_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    user = User(**{k: fetched_user[k] for k in ("username", "role", "scopes", "name", "email")})
    access_token = auth_service.create_token(
        {"sub": user.username, "scopes": user.scopes},
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
