"""
Integration tests for FastAPI /api/v1/inspect endpoint and error taxonomy.
"""
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.validation.url_validator import URLValidator
from app.models.inspection import InspectionResult

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


def test_invalid_url_abc_taxonomy():
    response = client.post("/api/v1/inspect", json={"url": "abc"})
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error_code"] == "INVALID_URL_FORMAT"
    assert detail["url_valid"] is False


def test_invalid_url_def_taxonomy():
    response = client.post("/api/v1/inspect", json={"url": "def"})
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


def test_valid_github_url_validation():
    normalized = URLValidator.validate_and_normalize("github.com")
    assert normalized == "https://github.com/"

    normalized_https = URLValidator.validate_and_normalize("https://github.com")
    assert normalized_https == "https://github.com/"


@patch("app.inspection.engine.InspectionEngine.inspect", new_callable=AsyncMock)
def test_valid_github_inspect_endpoint(mock_inspect):
    mock_inspect.return_value = InspectionResult(
        url="https://github.com/",
        final_url="https://github.com/",
        status_code=200,
        response_time_ms=250.0,
        html_content="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>GitHub: Let’s build from here</title>
            <meta name="description" content="GitHub is where over 100 million developers shape the future of software, together.">
        </head>
        <body>
            <h1>Build software better, together</h1>
            <p>GitHub provides developer tools and cloud platform for hosting repositories and building software together.</p>
        </body>
        </html>
        """
    )
    response = client.post("/api/v1/inspect", json={"url": "https://github.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "https://github.com/"
    assert "scores" in data
    assert "technical_metrics" in data
    assert data["technical_metrics"]["status_code"] == 200

