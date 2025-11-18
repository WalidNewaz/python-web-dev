import pytest
from fastapi import HTTPException
from fastapi_todo.dependencies import get_api_key

def test_get_api_key_valid():
    """Should return the key when correct."""
    result = get_api_key("secret-key")
    assert result == "secret-key"

def test_get_api_key_invalid_raises():
    """Should raise HTTPException for invalid key."""
    with pytest.raises(HTTPException) as exc_info:
        get_api_key("wrong-key")

    exc = exc_info.value
    assert exc.status_code == 403
    assert "Invalid API key" in exc.detail
