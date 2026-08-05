"""
API Request DTOs.
"""
from pydantic import BaseModel, Field


class InspectionRequest(BaseModel):
    url: str = Field(..., description="Target website URL to inspect (e.g. https://example.com)", json_schema_extra={"example": "https://example.com"})
