"""
Models representing explainable evidence items and bundles.
"""
from typing import List, Union
from pydantic import BaseModel, Field
from app.shared.enums import Severity, Category


class Evidence(BaseModel):
    issue: str
    category: Category
    severity: Severity
    observed_value: Union[int, float, str, bool]
    expected_value: str
    recommendation: str


class EvidenceBundle(BaseModel):
    url: str
    overall_score: int
    failed_evidences: List[Evidence] = Field(default_factory=list)
    passed_evidences: List[Evidence] = Field(default_factory=list)
