"""
Application domain Enums.
"""
from enum import Enum


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Category(str, Enum):
    SEO = "seo"
    PERFORMANCE = "performance"
    ACCESSIBILITY = "accessibility"
    CONTENT = "content"


class InspectionStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
