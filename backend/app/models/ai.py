"""
Models representing AI summary results and verification outcomes.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class AISummaryResult(BaseModel):
    executive_summary: str
    key_strengths: List[str] = Field(default_factory=list)
    prioritized_issues: List[str] = Field(default_factory=list)
    action_plan: List[str] = Field(default_factory=list)


class VerificationResult(BaseModel):
    is_valid: bool
    rejection_reason: Optional[str] = None
    verified_summary: Optional[AISummaryResult] = None
