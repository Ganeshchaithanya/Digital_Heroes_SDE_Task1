"""
Models representing evaluation results and scored findings.
"""
from typing import List, Dict, Any, Union
from pydantic import BaseModel, Field
from app.shared.enums import Severity, Category


class Finding(BaseModel):
    policy_name: str
    category: Category
    severity: Severity
    observed_value: Union[int, float, str, bool]
    expected_value: str
    passed: bool
    recommendation: str
    weight: int = 1


class CategoryScore(BaseModel):
    category: Category
    score: int  # 0 to 100
    passed_count: int = 0
    total_count: int = 0


class EvaluationResult(BaseModel):
    overall_score: int  # 0 to 100
    category_scores: Dict[Category, CategoryScore] = Field(default_factory=dict)
    findings: List[Finding] = Field(default_factory=list)
