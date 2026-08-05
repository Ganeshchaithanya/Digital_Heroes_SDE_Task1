"""
Validation Layer: URL Syntax Validation and Normalization.
Does NOT execute any HTTP downloads.
"""
from urllib.parse import urlparse, urlunparse
from app.shared.constants import ALLOWED_SCHEMES
from app.shared.exceptions import (
    URLValidationError,
    MalformedURLError,
    UnsupportedProtocolError,
    SSRFRestrictedError
)
from app.observability.logger import logger


class URLValidator:
    """
    Validates URL syntax, protocol schemes, and normalizes URL inputs.
    """

    @staticmethod
    def validate_and_normalize(raw_url: str) -> str:
        if not raw_url or not isinstance(raw_url, str):
            raise MalformedURLError("URL input must be a non-empty string.")

        cleaned_url = raw_url.strip()
        if not cleaned_url:
            raise MalformedURLError("URL cannot be blank or whitespace.")

        # Check scheme if a protocol prefix exists (e.g., scheme:...)
        if ":" in cleaned_url:
            possible_scheme = cleaned_url.split(":", 1)[0].lower()
            if possible_scheme.isalnum():
                if possible_scheme not in ALLOWED_SCHEMES:
                    raise UnsupportedProtocolError(
                        f"Unsupported scheme '{possible_scheme}'. Only HTTP and HTTPS protocols are allowed."
                    )
        else:
            cleaned_url = "https://" + cleaned_url

        try:
            parsed = urlparse(cleaned_url)
        except Exception as e:
            raise MalformedURLError(f"Malformed URL string: {str(e)}") from e

        scheme = (parsed.scheme or "").lower()
        if scheme not in ALLOWED_SCHEMES:
            raise UnsupportedProtocolError(
                f"Unsupported scheme '{scheme}'. Only HTTP and HTTPS protocols are allowed."
            )

        hostname = (parsed.hostname or "").lower()
        if not hostname:
            raise MalformedURLError("URL must contain a valid domain name or hostname.")

        if "." not in hostname and hostname != "localhost":
            raise MalformedURLError(f"Invalid domain name or hostname '{hostname}'.")

        # Disallow private range to prevent SSRF
        if hostname.startswith(("0.", "127.", "169.254.", "192.168.", "10.")):
            logger.warning(f"Prevented private subnet access attempt: {hostname}")
            raise SSRFRestrictedError("Access to private/local network IP addresses is restricted for security.")

        path = parsed.path or "/"
        
        normalized = urlunparse((
            scheme,
            parsed.netloc.lower(),
            path,
            parsed.params,
            parsed.query,
            ""  # Strip URL fragment (# anchor)
        ))

        return normalized
