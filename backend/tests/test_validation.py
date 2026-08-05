"""
Unit tests for Module 1: Validation Layer.
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.validation.url_validator import URLValidator
from app.shared.exceptions import URLValidationError


def test_valid_url_normalization():
    assert URLValidator.validate_and_normalize("example.com") == "https://example.com/"
    assert URLValidator.validate_and_normalize("http://example.com") == "http://example.com/"
    assert URLValidator.validate_and_normalize("HTTPS://EXAMPLE.COM/test#anchor") == "https://example.com/test"


def test_invalid_url_schemes():
    with pytest.raises(URLValidationError, match="Unsupported scheme"):
        URLValidator.validate_and_normalize("ftp://example.com")

    with pytest.raises(URLValidationError, match="Unsupported scheme"):
        URLValidator.validate_and_normalize("javascript:alert(1)")


def test_blank_urls():
    with pytest.raises(URLValidationError, match="non-empty string"):
        URLValidator.validate_and_normalize("")


def test_private_ip_rejection():
    with pytest.raises(URLValidationError, match="restricted"):
        URLValidator.validate_and_normalize("http://127.0.0.1")
