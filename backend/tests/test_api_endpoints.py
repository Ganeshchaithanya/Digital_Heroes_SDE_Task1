"""
Integration tests for FastAPI /api/v1/inspect endpoint and error taxonomy.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["project"] == "PAGEPULSE"
    assert json_data["status"] == "online"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_invalid_url_format_taxonomy():
    response = client.post("/api/v1/inspect", json={"url": "not-a-valid-url"})
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error_code"] == "INVALID_URL_FORMAT"
    assert detail["url_valid"] is False


def test_unsupported_protocol_taxonomy():
    response = client.post("/api/v1/inspect", json={"url": "ftp://example.com"})
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error_code"] == "UNSUPPORTED_PROTOCOL"
    assert detail["url_valid"] is False


def test_ssrf_restricted_network_taxonomy():
    response = client.post("/api/v1/inspect", json={"url": "http://127.0.0.1:8000"})
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error_code"] == "RESTRICTED_NETWORK_ACCESS"
    assert detail["url_valid"] is False
