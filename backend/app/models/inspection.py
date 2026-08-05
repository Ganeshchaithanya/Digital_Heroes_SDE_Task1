"""
Model representing raw network inspection result.
"""
from typing import Dict
from pydantic import BaseModel, Field


class InspectionResult(BaseModel):
    url: str
    final_url: str
    status_code: int
    response_time_ms: float
    headers: Dict[str, str] = Field(default_factory=dict)
    content_type: str = ""
    html_content: str = ""
