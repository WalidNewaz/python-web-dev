# ============================================================
# Core Security ops
# ============================================================
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash plain password using bcrypt."""
    return pwd_context.hash(password)