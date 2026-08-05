"""
Validation Layer: URL Syntax Validation and Normalization.
Does NOT execute any HTTP downloads.
"""
from urllib.parse import urlparse, urlunparse
from app.shared.constants import ALLOWED_SCHEMES
from app.shared.exceptions import URLValidationError
from app.observability.logger import logger


class URLValidator:
    """
    Validates URL syntax, protocol schemes, and normalizes URL inputs.
    """

    @staticmethod
    def validate_and_normalize(raw_url: str) -> str:
        if not raw_url or not isinstance(raw_url, str):
            raise URLValidationError("URL input must be a non-empty string.")

        cleaned_url = raw_url.strip()
        if not cleaned_url:
            raise URLValidationError("URL cannot be blank or whitespace.")

        # Check scheme if a protocol prefix exists (e.g., scheme:...)
        if ":" in cleaned_url:
            possible_scheme = cleaned_url.split(":", 1)[0].lower()
            if possible_scheme.isalnum():
                if possible_scheme not in ALLOWED_SCHEMES:
                    raise URLValidationError(
                        f"Unsupported scheme '{possible_scheme}'. Only HTTP and HTTPS are permitted."
                    )
        else:
            cleaned_url = "https://" + cleaned_url

        try:
            parsed = urlparse(cleaned_url)
        except Exception as e:
            raise URLValidationError(f"Malformed URL string: {str(e)}") from e

        scheme = (parsed.scheme or "").lower()
        if scheme not in ALLOWED_SCHEMES:
            raise URLValidationError(
                f"Unsupported scheme '{scheme}'. Only HTTP and HTTPS are permitted."
            )

        hostname = (parsed.hostname or "").lower()
        if not hostname:
            raise URLValidationError("URL must contain a valid domain name or hostname.")

        # Basic domain format sanity check
        if "." not in hostname and hostname != "localhost":
            raise URLValidationError(f"Invalid domain name '{hostname}'.")

        # Disallow invalid characters or local IP ranges if needed
        if hostname.startswith(("0.", "127.", "169.254.", "192.168.", "10.")):
            logger.warning(f"Prevented potential private subnet access attempt: {hostname}")
            # Note: We can allow or disallow depending on assignment rules. We disallow private range to prevent SSRF.
            raise URLValidationError("Access to private/local network IP addresses is restricted.")

        # Normalize URL path (default to / if empty)
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
