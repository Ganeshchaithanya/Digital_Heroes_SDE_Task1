"""
FastAPI V1 Inspection Endpoint.
"""
from fastapi import APIRouter, HTTPException, status
from app.schemas.request import InspectionRequest
from app.schemas.response import InspectionResponse
from app.services.inspection_service import InspectionService
from app.shared.exceptions import URLValidationError, InspectionFetchError
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

    except URLValidationError as e:
        logger.warning(f"URL validation error for input '{request.url}': {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "URL_VALIDATION_ERROR", "message": e.message, "details": e.details}
        )
    except InspectionFetchError as e:
        logger.error(f"Network inspection error for input '{request.url}': {e.message}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"error": "FETCH_FAILED", "message": e.message, "details": e.details}
        )
    except Exception as e:
        logger.exception(f"Unhandled error inspecting URL '{request.url}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "INTERNAL_SERVER_ERROR", "message": str(e)}
        )
