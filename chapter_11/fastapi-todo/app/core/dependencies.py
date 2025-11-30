from fastapi import HTTPException, Header

# Route dependency
def get_api_key(x_api_key: str = Header(...)) -> str:
    """Simple dependency to check for API key header."""
    if x_api_key != "secret-key":
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API key")
    return x_api_key
