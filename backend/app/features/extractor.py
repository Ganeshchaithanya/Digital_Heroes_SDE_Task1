"""
Main Feature Extractor Coordinator.
Aggregates specialized extractors into a strongly-typed FeatureVector.
Calculates quantitative metrics only. No policy evaluation.
"""
from app.models.inspection import InspectionResult
from app.models.document import PageDocument
from app.models.features import FeatureVector
from app.features.seo import SEOFeatureExtractor
from app.features.performance import PerformanceFeatureExtractor
from app.features.content import ContentFeatureExtractor
from app.observability.logger import logger


class FeatureExtractor:
    """
    Coordinates sub-extractors to build a complete FeatureVector.
    """

    @staticmethod
    def extract_features(
        document: PageDocument,
        inspection_result: InspectionResult
    ) -> FeatureVector:
        seo_data = SEOFeatureExtractor.extract(document)
        perf_data = PerformanceFeatureExtractor.extract(inspection_result)
        content_data = ContentFeatureExtractor.extract(document)

        combined = {**seo_data, **perf_data, **content_data}
        
        feature_vector = FeatureVector.model_validate(combined)
        logger.info(f"Derived FeatureVector: {feature_vector.model_dump()}")
        return feature_vector
