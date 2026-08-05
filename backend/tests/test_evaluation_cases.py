"""
Unit Tests for PAGEPULSE Evaluation Engine:
- Case 1: Healthy Website (High Score >= 90)
- Case 2: Non-Healthy Website 1 (SEO & Content Failures)
- Case 3: Non-Healthy Website 2 (Accessibility & Performance Failures)
"""
import pytest
from app.models.inspection import InspectionResult
from app.parser.html_parser import HTMLParser
from app.features.extractor import FeatureExtractor
from app.policies.loader import PolicyLoader
from app.evaluation.evaluator import EvaluationEngine
from app.shared.enums import Category


class TestEvaluationCases:

    @pytest.fixture(autouse=True)
    def setup_policies(self):
        self.policies = PolicyLoader("v1").load_policies()
        self.evaluator = EvaluationEngine(self.policies)

    def test_healthy_website_case(self, healthy_website_html):
        """
        CASE 1: HEALTHY WEBSITE
        Expected: Overall score >= 90 (Good Health)
        """
        inspection_result = InspectionResult(
            url="https://healthy-example.com",
            final_url="https://healthy-example.com",
            status_code=200,
            response_time_ms=450.0,
            html_content=healthy_website_html
        )

        doc = HTMLParser.parse(inspection_result)
        features = FeatureExtractor.extract_features(doc, inspection_result)
        evaluation = self.evaluator.evaluate(features)

        # Assertions for Healthy Case
        assert evaluation.overall_score >= 90
        assert evaluation.category_scores[Category.SEO].score >= 90
        assert evaluation.category_scores[Category.PERFORMANCE].score == 100
        assert evaluation.category_scores[Category.ACCESSIBILITY].score == 100
        assert evaluation.category_scores[Category.CONTENT].score == 100
        assert len(evaluation.findings) == 6

    def test_non_healthy_seo_content_case(self, non_healthy_seo_html):
        """
        CASE 2: NON-HEALTHY WEBSITE 1 (SEO & Content Failures)
        Expected: Reduced overall score due to 4 H1 tags, short title, missing description, low word count.
        """
        inspection_result = InspectionResult(
            url="https://bad-seo-example.com",
            final_url="https://bad-seo-example.com",
            status_code=200,
            response_time_ms=500.0,
            html_content=non_healthy_seo_html
        )

        doc = HTMLParser.parse(inspection_result)
        features = FeatureExtractor.extract_features(doc, inspection_result)
        evaluation = self.evaluator.evaluate(features)

        # Assertions for SEO & Content Non-Healthy Case
        assert evaluation.overall_score < 60
        assert evaluation.category_scores[Category.SEO].score < 30
        assert evaluation.category_scores[Category.CONTENT].score < 10
        
        # Check specific findings
        findings_map = {f.policy_name: f for f in evaluation.findings}
        assert findings_map["h1_count"].passed is False
        assert findings_map["meta_description"].passed is False
        assert findings_map["word_count"].passed is False

    def test_non_healthy_accessibility_performance_case(self, non_healthy_accessibility_html):
        """
        CASE 3: NON-HEALTHY WEBSITE 2 (Accessibility & Performance Failures)
        Expected: Reduced score due to 5 missing image ALT attributes and slow network response (3500ms).
        """
        inspection_result = InspectionResult(
            url="https://slow-inaccessible-example.com",
            final_url="https://slow-inaccessible-example.com",
            status_code=200,
            response_time_ms=3500.0,  # 3.5 seconds (exceeds 2000ms limit)
            html_content=non_healthy_accessibility_html
        )

        doc = HTMLParser.parse(inspection_result)
        features = FeatureExtractor.extract_features(doc, inspection_result)
        evaluation = self.evaluator.evaluate(features)

        # Assertions for Accessibility & Performance Non-Healthy Case
        assert evaluation.category_scores[Category.PERFORMANCE].score < 50
        
        findings_map = {f.policy_name: f for f in evaluation.findings}
        assert findings_map["image_alt"].passed is False
        assert findings_map["response_time"].passed is False
