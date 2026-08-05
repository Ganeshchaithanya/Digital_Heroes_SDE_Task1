"""
Inspection Engine: Asynchronous HTTP Network Inspector.
Does NOT parse HTML content.
"""
import time
import httpx
from app.models.inspection import InspectionResult
from app.shared.exceptions import (
    InspectionFetchError,
    RequestTimeoutError,
    DNSFailureError,
    ConnectionRefusedError,
    SSLError
)
from app.core.config import settings
from app.observability.logger import logger


class InspectionEngine:
    """
    Executes HTTP GET request to download webpage and collect performance metadata.
    """

    def __init__(
        self,
        timeout_seconds: float = settings.HTTP_TIMEOUT_SECONDS,
        user_agent: str = settings.USER_AGENT
    ):
        self.timeout_seconds = timeout_seconds
        self.headers = {"User-Agent": user_agent}

    async def inspect(self, url: str) -> InspectionResult:
        logger.info(f"Starting inspection HTTP request for URL: {url}")
        start_time = time.perf_counter()

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout_seconds, connect=5.0),
                follow_redirects=True,
                headers=self.headers
            ) as client:
                response = await client.get(url)
                end_time = time.perf_counter()
                latency_ms = round((end_time - start_time) * 1000, 2)

                headers_dict = {k: v for k, v in response.headers.items()}
                content_type = headers_dict.get("content-type", "").lower()
                html_content = response.text if "text/html" in content_type or "application/xhtml" in content_type or not content_type else response.text

                logger.info(f"Fetched {url} - Status: {response.status_code}, Latency: {latency_ms}ms")

                return InspectionResult(
                    url=url,
                    final_url=str(response.url),
                    status_code=response.status_code,
                    response_time_ms=latency_ms,
                    headers=headers_dict,
                    content_type=content_type,
                    html_content=html_content
                )

        except httpx.TimeoutException as e:
            logger.error(f"Timeout inspecting URL {url}: {e}")
            raise RequestTimeoutError(
                f"Request timed out after {self.timeout_seconds} seconds.",
                details={"url": url, "timeout_seconds": self.timeout_seconds}
            ) from e
        except httpx.SSLError as e:
            logger.error(f"SSL certificate error inspecting URL {url}: {e}")
            raise SSLError(
                "SSL certificate validation failed for target domain.",
                details={"url": url, "error": str(e)}
            ) from e
        except httpx.ConnectError as e:
            err_msg = str(e).lower()
            logger.error(f"Connection error inspecting URL {url}: {e}")
            if "name or service not known" in err_msg or "getaddrinfo failed" in err_msg or "dns" in err_msg:
                raise DNSFailureError(
                    "Unable to resolve domain name. Check domain spelling.",
                    details={"url": url, "error": str(e)}
                ) from e
            else:
                raise ConnectionRefusedError(
                    "Target server refused connection or domain is unreachable.",
                    details={"url": url, "error": str(e)}
                ) from e
        except httpx.HTTPError as e:
            logger.error(f"HTTP error inspecting URL {url}: {e}")
            raise InspectionFetchError(
                f"Failed to fetch webpage: {str(e)}",
                details={"url": url, "error": str(e)}
            ) from e
        except Exception as e:
            logger.error(f"Unexpected network error fetching {url}: {e}")
            raise InspectionFetchError(
                f"Unexpected error inspecting URL: {str(e)}",
                details={"url": url, "error": str(e)}
            ) from e
