"""
FastAPI V1 Inspection Endpoint.
Implements precise error taxonomy & status mapping.
"""
from fastapi import APIRouter, HTTPException, status
from app.schemas.request import InspectionRequest
from app.schemas.response import InspectionResponse
from app.services.inspection_service import InspectionService
from app.shared.exceptions import (
    URLValidationError,
    MalformedURLError,
    UnsupportedProtocolError,
    SSRFRestrictedError,
    InspectionFetchError,
    DNSFailureError,
    ConnectionRefusedError,
    SSLError,
    RequestTimeoutError
)
from app.observability.logger import logger

router = APIRouter(tags=["Inspection"])


@router.post(
    "/inspect",
    response_model=InspectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Inspect a website URL",
    description="Validates URL, fetches HTML, calculates technical metrics, evaluates policies, and generates AI explanations."
)
async def inspect_url(request: InspectionRequest) -> InspectionResponse:
    service = InspectionService()
    try:
        response = await service.inspect(request.url)
        return response

    # --- Validation Layer Exceptions (HTTP 400) ---
    except MalformedURLError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INVALID_URL_FORMAT",
                "status_name": "❌ Invalid URL Format",
                "url_valid": False,
                "message": e.message,
                "details": e.details
            }
        )
    except UnsupportedProtocolError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "UNSUPPORTED_PROTOCOL",
                "status_name": "❌ Unsupported Protocol",
                "url_valid": False,
                "message": e.message,
                "details": e.details
            }
        )
    except SSRFRestrictedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "RESTRICTED_NETWORK_ACCESS",
                "status_name": "❌ Restricted Network Access",
                "url_valid": False,
                "message": e.message,
                "details": e.details
            }
        )
    except URLValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "URL_VALIDATION_ERROR",
                "status_name": "❌ Invalid URL",
                "url_valid": False,
                "message": e.message,
                "details": e.details
            }
        )

    # --- Network Inspection Exceptions (HTTP 502 / 504) ---
    except DNSFailureError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error_code": "DOMAIN_NOT_FOUND",
                "status_name": "❌ Domain Not Found",
                "url_valid": True,
                "message": e.message,
                "details": e.details
            }
        )
    except ConnectionRefusedError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error_code": "SERVER_UNREACHABLE",
                "status_name": "❌ Server Unreachable",
                "url_valid": True,
                "message": e.message,
                "details": e.details
            }
        )
    except SSLError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error_code": "SSL_ERROR",
                "status_name": "❌ SSL Certificate Error",
                "url_valid": True,
                "message": e.message,
                "details": e.details
            }
        )
    except RequestTimeoutError as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={
                "error_code": "REQUEST_TIMED_OUT",
                "status_name": "⚠ Request Timed Out",
                "url_valid": True,
                "message": e.message,
                "details": e.details
            }
        )
    except InspectionFetchError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error_code": "FETCH_FAILED",
                "status_name": "❌ Inspection Fetch Failed",
                "url_valid": True,
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        logger.exception(f"Unhandled error inspecting URL '{request.url}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "INTERNAL_SERVER_ERROR",
                "status_name": "❌ Server Internal Error",
                "url_valid": True,
                "message": str(e)
            }
        )
