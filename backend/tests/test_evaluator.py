"""
Unit tests for Module 5 & 6: Policy Loader and Evaluation Engine.
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.policies.loader import PolicyLoader
from app.models.features import FeatureVector
from app.evaluation.evaluator import EvaluationEngine
from app.evaluation.evidence_generator import EvidenceGenerator


def test_policy_loader_and_evaluation():
    loader = PolicyLoader(version="v1")
    policies = loader.load_policies()
    assert len(policies) >= 6

    # Test passing feature vector
    perfect_fv = FeatureVector(
        title_length=45,
        meta_description_length=120,
        h1_count=1,
        missing_alt_images_count=0,
        response_time_ms=500.0,
        word_count=500,
        status_code=200
    )

    evaluator = EvaluationEngine(policies)
    result = evaluator.evaluate(perfect_fv)

    assert result.overall_score == 100
    assert all(f.passed for f in result.findings)

    bundle = EvidenceGenerator.generate_bundle("https://test.com", result)
    assert len(bundle.failed_evidences) == 0
    assert len(bundle.passed_evidences) >= 5


def test_failing_evaluation():
    loader = PolicyLoader(version="v1")
    policies = loader.load_policies()

    failing_fv = FeatureVector(
        title_length=5,               # Too short (fails title_length)
        meta_description_length=0,    # Fails meta_description
        h1_count=0,                   # Fails h1_count
        missing_alt_images_count=5,   # Fails image_alt
        response_time_ms=3500.0,      # Fails response_time
        word_count=50,                # Fails word_count
        status_code=200
    )

    evaluator = EvaluationEngine(policies)
    result = evaluator.evaluate(failing_fv)

    assert result.overall_score < 50
    bundle = EvidenceGenerator.generate_bundle("https://test.com", result)
    assert len(bundle.failed_evidences) >= 5
