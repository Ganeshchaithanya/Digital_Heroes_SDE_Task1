"""
Integration tests for FastAPI /api/v1/inspect endpoint.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.models.inspection import InspectionResult

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_inspect_invalid_url():
    response = client.post("/api/v1/inspect", json={"url": "ftp://invalid-scheme.com"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error"] == "URL_VALIDATION_ERROR"


@patch("app.inspection.engine.InspectionEngine.inspect")
def test_inspect_successful_pipeline(mock_inspect):
    sample_html = """
    <html>
    <head><title>A Great Website Title For Testing Purpose</title></head>
    <body>
        <h1>Main Page Title</h1>
        <p>Short paragraph text for word count testing.</p>
    </body>
    </html>
    """
    mock_inspect.return_value = InspectionResult(
        url="https://example.com",
        final_url="https://example.com/",
        status_code=200,
        response_time_ms=120.0,
        html_content=sample_html
    )

    response = client.post("/api/v1/inspect", json={"url": "https://example.com"})
    assert response.status_code == 200

    data = response.json()
    assert data["url"] == "https://example.com/"
    assert "technical_metrics" in data
    assert "scores" in data
    assert "issues" in data
    assert "recommendations" in data
    assert data["technical_metrics"]["h1_count"] == 1
