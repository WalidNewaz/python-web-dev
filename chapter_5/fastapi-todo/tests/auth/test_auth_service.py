import pytest
from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
from jose import jwt

from app.core.security import get_pwd_ctx
from app.auth.service import AuthService, SECRET_KEY, ALGORITHM
from app.auth.dependencies import get_current_user, authenticate_basic


# Define a fixture to instantiate the service
@pytest.fixture(scope="module")
def auth_service():
    pwd_context = get_pwd_ctx()
    service_instance = AuthService(pwd_context=pwd_context)
    return service_instance


def test_create_and_decode_access_token(auth_service):
    data = {"sub": "alice"}
    token = auth_service.create_token(data)
    payload = auth_service.decode_token(token)
    assert payload["sub"] == "alice"
    assert "exp" in payload


def test_decode_access_token_invalid(auth_service):
    """Should raise if token is malformed."""
    with pytest.raises(HTTPException) as exc_info:
        auth_service.decode_token("not-a-jwt")
    assert exc_info.value.status_code == 401
    assert "Invalid or expired token" in exc_info.value.detail


def test_get_current_user_valid(auth_service):
    """Directly test logic of get_current_user with a valid token."""
    token = auth_service.create_token({"sub": "bob"})
    username = get_current_user(token=token)
    assert username == "bob"


def test_get_current_user_invalid(auth_service ):
    """Should raise if token missing 'sub'."""
    bad_token = jwt.encode(
        {"no_sub": "x"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=bad_token)
    assert exc_info.value.status_code == 401

def test_authenticate_success(auth_service ):
    creds = HTTPBasicCredentials(username="admin", password="secret")
    result = authenticate_basic(creds)
    assert result == "admin"

def test_authenticate_wrong_username(auth_service ):
    creds = HTTPBasicCredentials(username="user", password="secret")
    with pytest.raises(HTTPException) as excinfo:
        authenticate_basic(creds)
    exc = excinfo.value
    assert exc.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.detail == "Incorrect username or password"
    assert exc.headers["WWW-Authenticate"] == 'Basic realm=\"Restricted\"'

def test_authenticate_wrong_password(auth_service ):
    creds = HTTPBasicCredentials(username="admin", password="wrong")
    with pytest.raises(HTTPException) as excinfo:
        authenticate_basic(creds)
    exc = excinfo.value
    assert exc.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.detail == "Incorrect username or password"
    assert exc.headers["WWW-Authenticate"] == 'Basic realm=\"Restricted\"'

def test_authenticate_both_wrong(auth_service ):
    creds = HTTPBasicCredentials(username="foo", password="bar")
    with pytest.raises(HTTPException) as excinfo:
        authenticate_basic(creds)
    assert excinfo.value.status_code == 401

def test_authenticate_empty_credentials(auth_service ):
    creds = HTTPBasicCredentials(username="", password="")
    with pytest.raises(HTTPException):
        authenticate_basic(creds)