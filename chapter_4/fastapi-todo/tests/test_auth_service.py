import pytest
from fastapi import HTTPException
from fastapi_todo import auth_service


def test_get_password_hash_and_verify():
    password = "wonderland"
    hashed = auth_service.get_password_hash(password)
    assert hashed != password
    assert auth_service.verify_password(password, hashed)
    assert not auth_service.verify_password("wrong", hashed)


def test_create_and_decode_access_token():
    data = {"sub": "alice"}
    token = auth_service.create_access_token(data)
    payload = auth_service.decode_access_token(token)
    assert payload["sub"] == "alice"
    assert "exp" in payload


def test_decode_access_token_invalid():
    """Should raise if token is malformed."""
    with pytest.raises(HTTPException) as exc_info:
        auth_service.decode_access_token("not-a-jwt")
    assert exc_info.value.status_code == 401
    assert "Invalid or expired token" in exc_info.value.detail


def test_get_current_user_valid(monkeypatch):
    """Directly test logic of get_current_user with a valid token."""
    token = auth_service.create_access_token({"sub": "bob"})
    username = auth_service.get_current_user(token=token)
    assert username == "bob"


def test_get_current_user_invalid(monkeypatch):
    """Should raise if token missing 'sub'."""
    bad_token = auth_service.jwt.encode(
        {"no_sub": "x"},
        auth_service.SECRET_KEY,
        algorithm=auth_service.ALGORITHM,
    )

    with pytest.raises(auth_service.HTTPException) as exc_info:
        auth_service.get_current_user(token=bad_token)
    assert exc_info.value.status_code == 401
