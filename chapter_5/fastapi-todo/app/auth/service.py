# ============================================================
# Business logic
# ============================================================
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, HTTPBasicCredentials, HTTPBasic
from typing import Optional, Dict
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import secrets

from app.users.schemas import User


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
SECRET_KEY = "super-secret-key"       # In real apps, load from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        "read": "Read access to resources",
        "write": "Write access to resources",
        "admin": "Administrative access"
    })

basic_auth_scheme = HTTPBasic()



class AuthService:
    def __init__(self, pwd_context):
        self.pwd_context = pwd_context

    # ---------------------------------------------------------------------
    # Password hashing and verification
    # ---------------------------------------------------------------------

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify plain password against hashed password."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str, users: Dict) -> Optional[User]:
        user = users.get(username)
        if not user or not self.verify_password(password, user["hashed_password"]):
            return None
        return User(**{k: user[k] for k in ("username", "role", "scopes", "name", "email")})

    # ---------------------------------------------------------------------
    # Token creation and decoding
    # ---------------------------------------------------------------------

    @staticmethod
    def decode_token(token: str) -> Dict:
        """Decode JWT token; raise HTTPException if invalid or expired."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    @staticmethod
    def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT token with optional expiration delta."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_access_token_from_refresh(refresh_token: str) -> str:
        """Create JWT token from a refresh token."""
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "refresh":
                raise HTTPException(status_code=401, detail="Invalid refresh token")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        new_access_token = AuthService.create_token(
            {"sub": payload.get('sub'), "scopes": payload.get("scopes")},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return new_access_token

    # ---------------------------------------------------------------------
    # Dependency
    # ---------------------------------------------------------------------

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
        """Extract 'sub' (username) from JWT token."""
        payload = AuthService.decode_token(token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username

    @staticmethod
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
