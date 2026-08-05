"""
Policy JSON validation schema.
"""
from typing import Optional, Union, Any, List
from pydantic import BaseModel, Field
from app.shared.enums import Severity, Category


class PolicyRule(BaseModel):
    name: str
    feature: str
    category: Category
    severity: Severity
    weight: int = Field(default=1, ge=1, le=10)
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    exact_value: Optional[Any] = None
    allowed_values: Optional[List[Any]] = None
    disallowed_values: Optional[List[Any]] = None
    recommendation: str
    expected_display: str
