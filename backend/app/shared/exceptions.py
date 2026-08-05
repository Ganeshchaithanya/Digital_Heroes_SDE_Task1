"""
Custom Exception hierarchy for PAGEPULSE.
Provides specialized exceptions for exact error taxonomy.
"""
from typing import Optional, Dict, Any


class PagePulseException(Exception):
    """Base exception for PAGEPULSE application."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


# --- Validation Layer Exceptions ---

class URLValidationError(PagePulseException):
    """Base URL validation exception."""
    pass


class MalformedURLError(URLValidationError):
    """Raised when URL syntax is malformed."""
    pass


class UnsupportedProtocolError(URLValidationError):
    """Raised when URL scheme is not HTTP or HTTPS."""
    pass


class SSRFRestrictedError(URLValidationError):
    """Raised when URL targets restricted private network IP ranges."""
    pass


# --- Inspection Engine Exceptions ---

class InspectionFetchError(PagePulseException):
    """Base network fetch exception."""
    pass


class DNSFailureError(InspectionFetchError):
    """Raised when domain DNS resolution fails."""
    pass


class ConnectionRefusedError(InspectionFetchError):
    """Raised when target server actively refuses connection."""
    pass


class SSLError(InspectionFetchError):
    """Raised when SSL/TLS certificate validation fails."""
    pass


class RequestTimeoutError(InspectionFetchError):
    """Raised when HTTP GET request times out."""
    pass


# --- Other Module Exceptions ---

class HTMLParseError(PagePulseException):
    """Raised when HTML content cannot be parsed."""
    pass


class PolicyValidationError(PagePulseException):
    """Raised when policy JSON definition is invalid."""
    pass


class AIServiceError(PagePulseException):
    """Raised when Groq AI generation or verification fails."""
    pass
