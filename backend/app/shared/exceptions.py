"""
Custom Exception hierarchy for PAGEPULSE.
"""
from typing import Optional, Dict, Any


class PagePulseException(Exception):
    """Base exception for PAGEPULSE application."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class URLValidationError(PagePulseException):
    """Raised when URL syntax validation fails or protocol is unsupported."""
    pass


class InspectionFetchError(PagePulseException):
    """Raised when webpage HTTP fetch fails (timeout, connection error, DNS failure)."""
    pass


class HTMLParseError(PagePulseException):
    """Raised when HTML content cannot be parsed."""
    pass


class PolicyValidationError(PagePulseException):
    """Raised when policy JSON definition is invalid."""
    pass


class AIServiceError(PagePulseException):
    """Raised when Groq AI generation or verification fails."""
    pass
