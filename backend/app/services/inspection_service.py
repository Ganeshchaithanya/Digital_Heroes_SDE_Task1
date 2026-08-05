"""
Inspection Service Layer.
Orchestrates the entire website inspection pipeline cleanly.
Exposes a single clean entrypoint: inspect(url) -> InspectionResponse
"""
from typing import List, Optional
from app.validation.url_validator import URLValidator
from app.inspection.engine import InspectionEngine
from app.parser.html_parser import HTMLParser
from app.features.extractor import FeatureExtractor
from app.policies.loader import PolicyLoader
from app.evaluation.evaluator import EvaluationEngine
from app.evaluation.evidence_generator import EvidenceGenerator
from app.ai.service import AIService
from app.schemas.response import (
    InspectionResponse,
    TechnicalMetricsDTO,
    CategoryScoresDTO,
    IssueDTO,
    AISummaryDTO
)
from app.shared.enums import Category
from app.observability.logger import logger


class InspectionService:
    """
    Service Layer Facade for PAGEPULSE inspection workflow.
    """

    def __init__(
        self,
        inspection_engine: Optional[InspectionEngine] = None,
        policy_loader: Optional[PolicyLoader] = None,
        ai_service: Optional[AIService] = None
    ):
        self.inspection_engine = inspection_engine or InspectionEngine()
        self.policy_loader = policy_loader or PolicyLoader()
        self.ai_service = ai_service or AIService()

    async def inspect(self, raw_url: str) -> InspectionResponse:
        logger.info(f"--- Starting Inspection Pipeline for '{raw_url}' ---")

        # 1. Validation Layer
        normalized_url = URLValidator.validate_and_normalize(raw_url)

        # 2. Inspection Engine
        inspection_result = await self.inspection_engine.inspect(normalized_url)

        # 3. HTML Parser
        page_document = HTMLParser.parse(inspection_result)

        # 4. Feature Extraction Subsystem
        feature_vector = FeatureExtractor.extract_features(page_document, inspection_result)

        # 5. Policy Loader
        policies = self.policy_loader.load_policies()

        # 6. Evaluation Engine
        evaluation_result = EvaluationEngine(policies).evaluate(feature_vector)

        # 7. Evidence Generator
        evidence_bundle = EvidenceGenerator.generate_bundle(normalized_url, evaluation_result)

        # 8. AI Service (Optional & Fail-safe)
        ai_summary_model = await self.ai_service.generate_ai_summary(evidence_bundle, feature_vector)

        # 9. Response Building Assembly
        response = self._build_response(
            url=normalized_url,
            feature_vector=feature_vector,
            evaluation_result=evaluation_result,
            evidence_bundle=evidence_bundle,
            ai_summary_model=ai_summary_model
        )

        logger.info(f"--- Completed Inspection Pipeline for '{normalized_url}' ---")
        return response

    @staticmethod
    def _build_response(
        url: str,
        feature_vector,
        evaluation_result,
        evidence_bundle,
        ai_summary_model
    ) -> InspectionResponse:
        # Technical Metrics DTO
        tech_metrics = TechnicalMetricsDTO(
            title_length=feature_vector.title_length,
            meta_description_length=feature_vector.meta_description_length,
            h1_count=feature_vector.h1_count,
            h2_count=feature_vector.h2_count,
            total_images_count=feature_vector.total_images_count,
            missing_alt_images_count=feature_vector.missing_alt_images_count,
            word_count=feature_vector.word_count,
            internal_links_count=feature_vector.internal_links_count,
            external_links_count=feature_vector.external_links_count,
            response_time_ms=feature_vector.response_time_ms,
            status_code=feature_vector.status_code
        )

        # Category Scores DTO
        cat_scores = CategoryScoresDTO(
            seo=evaluation_result.category_scores[Category.SEO].score,
            performance=evaluation_result.category_scores[Category.PERFORMANCE].score,
            accessibility=evaluation_result.category_scores[Category.ACCESSIBILITY].score,
            content=evaluation_result.category_scores[Category.CONTENT].score,
            overall=evaluation_result.overall_score
        )

        # Issues & Recommendations DTO
        issues_list: List[IssueDTO] = []
        recommendations_list: List[str] = []

        for ev in evidence_bundle.failed_evidences:
            issues_list.append(IssueDTO(
                issue=ev.issue,
                category=ev.category.value,
                severity=ev.severity.value,
                observed_value=ev.observed_value,
                expected_value=ev.expected_value,
                recommendation=ev.recommendation
            ))
            if ev.recommendation not in recommendations_list:
                recommendations_list.append(ev.recommendation)

        # AI Summary DTO if present
        ai_summary_dto = None
        if ai_summary_model:
            ai_summary_dto = AISummaryDTO(
                executive_summary=ai_summary_model.executive_summary,
                key_strengths=ai_summary_model.key_strengths,
                prioritized_issues=ai_summary_model.prioritized_issues,
                action_plan=ai_summary_model.action_plan
            )

        return InspectionResponse(
            url=url,
            technical_metrics=tech_metrics,
            scores=cat_scores,
            issues=issues_list,
            recommendations=recommendations_list,
            ai_summary=ai_summary_dto
        )
