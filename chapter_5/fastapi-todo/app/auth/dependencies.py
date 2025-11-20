# ============================================================
# Route dependencies
# ============================================================
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
import secrets

from app.core.security import get_pwd_ctx
from app.auth.service import AuthService, basic_auth_scheme
from app.users.service import UserService, get_user_service
from app.auth.service import oauth2_scheme

def get_auth_service(pwd_context=Depends(get_pwd_ctx)):
    return AuthService(pwd_context)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Extract 'sub' (username) from JWT token."""
    payload = AuthService.decode_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return username


def authenticate_basic(credentials: HTTPBasicCredentials = Depends(basic_auth_scheme)):
    """
    Performs basic auth authentication check.
    :param credentials:
    :return:
    """
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": 'Basic realm=\"Restricted\"'},
        )
    return credentials.username


def require_admin(
        username: str = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service),
):
    """Ensures that routes that dependent routes are only accessible to admins."""
    db_user = user_service.get_user(username=username)
    print("db_user", db_user)
    role = db_user.role
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
