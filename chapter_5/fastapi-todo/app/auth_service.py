from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import secrets
# from .models import User

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
SECRET_KEY = "super-secret-key"       # In real apps, load from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        "read": "Read access to resources",
        "write": "Write access to resources",
        "admin": "Administrative access"
    })

basic_auth_scheme = HTTPBasic()


# ---------------------------------------------------------------------
# Token creation and decoding
# ---------------------------------------------------------------------
def decode_token(token: str) -> Dict:
    """Decode JWT token; raise HTTPException if invalid or expired."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token with optional expiration delta."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ---------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Extract 'sub' (username) from JWT token."""
    payload = decode_token(token)
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
