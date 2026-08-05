"""
API Response DTOs.
Adheres strictly to the Digital Heroes assignment specification.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TechnicalMetricsDTO(BaseModel):
    title_length: int
    meta_description_length: int
    h1_count: int
    h2_count: int
    total_images_count: int
    missing_alt_images_count: int
    word_count: int
    internal_links_count: int
    external_links_count: int
    response_time_ms: float
    status_code: int


class CategoryScoresDTO(BaseModel):
    seo: int
    performance: int
    accessibility: int
    content: int
    overall: int


class IssueDTO(BaseModel):
    issue: str
    category: str
    severity: str
    observed_value: Any
    expected_value: str
    recommendation: str


class AISummaryDTO(BaseModel):
    executive_summary: str
    key_strengths: List[str]
    prioritized_issues: List[str]
    action_plan: List[str]


class InspectionResponse(BaseModel):
    url: str
    technical_metrics: TechnicalMetricsDTO
    scores: CategoryScoresDTO
    issues: List[IssueDTO]
    recommendations: List[str]
    ai_summary: Optional[AISummaryDTO] = None
