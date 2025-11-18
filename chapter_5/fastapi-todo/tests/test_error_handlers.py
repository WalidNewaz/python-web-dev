from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from app.error_handlers import (
    APIError,
    register_error_handlers,
)


def build_app():
    app = FastAPI()
    register_error_handlers(app)

    @app.get("/raise-http")
    def raise_http():
        raise HTTPException(status_code=404, detail="Not Found")

    @app.get("/raise-api")
    def raise_api():
        raise APIError(code=400, message="Bad API", details={"info": "x"})

    @app.get("/validation")
    def raise_validation(a: int):
        return {"a": a}

    return TestClient(app)


def test_http_exception_handler():
    client = build_app()
    response = client.get("/raise-http")
    assert response.status_code == 404
    assert response.json() == {"error": "Not Found"}


def test_api_error_handler():
    client = build_app()
    response = client.get("/raise-api")
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "Bad API"
    assert data["details"] == {"info": "x"}


def test_validation_exception_handler():
    client = build_app()
    # Missing required query param 'a' → triggers validation error
    response = client.get("/validation")
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation failed"
    assert isinstance(data["details"], list)
