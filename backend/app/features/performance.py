"""
Performance Feature Extractor.
Extracts response time and status code metrics from InspectionResult.
"""
from typing import Dict, Any
from app.models.inspection import InspectionResult


class PerformanceFeatureExtractor:
    """
    Extracts performance quantitative metrics from InspectionResult.
    """

    @staticmethod
    def extract(inspection_result: InspectionResult) -> Dict[str, Any]:
        return {
            "response_time_ms": inspection_result.response_time_ms,
            "status_code": inspection_result.status_code
        }
