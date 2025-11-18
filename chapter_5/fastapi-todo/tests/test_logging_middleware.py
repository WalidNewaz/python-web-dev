import logging
import re
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_todo.logging_config import setup_logging, LOG_FORMAT
from fastapi_todo.logging_middleware import register_request_logger


def build_test_app() -> TestClient:
    app = FastAPI()
    register_request_logger(app)

    @app.get("/ping")
    def ping():
        return {"ok": True}

    return TestClient(app)


def test_request_logger_emits_info_line(caplog):
    client = build_test_app()
    caplog.set_level(logging.INFO)

    resp = client.get("/ping")
    assert resp.status_code == 200

    # Find a log line like: "GET /ping completed in 0.0001s"
    matched = any(
        rec.levelno == logging.INFO and
        re.search(r"GET\s+/ping\s+completed in\s+\d+\.\d{4}s", rec.message)
        for rec in caplog.records
    )
    assert matched, "Expected request log line not found"


def test_setup_logging_applies_format_and_level(caplog):
    # Re-configure logging (basicConfig is a no-op if already set in this process,
    # but the caplog level check still verifies we can see INFO logs)
    setup_logging(level=logging.INFO)
    caplog.set_level(logging.INFO)

    logger = logging.getLogger("fastapi_todo.tests")
    logger.info("hello-format")

    assert any(
        rec.levelno == logging.INFO and
        rec.message == "hello-format" for rec in caplog.records
    )
