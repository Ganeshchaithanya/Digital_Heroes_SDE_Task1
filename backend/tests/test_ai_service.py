"""
Unit tests for Module 8, 9, 10 & 11: AI Subsystem and Fail-safe behavior.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.evidence import EvidenceBundle, Evidence
from app.models.features import FeatureVector
from app.shared.enums import Severity, Category
from app.ai.builder import PromptBuilder
from app.ai.verifier import Verifier
from app.ai.service import AIService


def test_prompt_builder():
    bundle = EvidenceBundle(
        url="https://test.com",
        overall_score=80,
        failed_evidences=[
            Evidence(
                issue="title_length",
                category=Category.SEO,
                severity=Severity.CRITICAL,
                observed_value=10,
                expected_value="30 to 60 characters",
                recommendation="Fix title length."
            )
        ]
    )

    prompt = PromptBuilder.build_prompt(bundle)
    assert "https://test.com" in prompt
    assert "title_length" in prompt
    assert "Fix title length." in prompt


def test_verifier_valid():
    valid_json = {
        "executive_summary": "The website has good performance but needs SEO fixes.",
        "key_strengths": ["Fast response time"],
        "prioritized_issues": ["Title length is too short"],
        "action_plan": ["Update page title tag"]
    }
    fv = FeatureVector()

    res = Verifier.verify(valid_json, fv)
    assert res.is_valid is True
    assert res.verified_summary.executive_summary == valid_json["executive_summary"]


@pytest.mark.asyncio
async def test_ai_service_fail_safe_on_exception():
    mock_provider = MagicMock()
    mock_provider.generate_summary = AsyncMock(side_effect=Exception("API limit exceeded"))

    service = AIService(provider=mock_provider)
    bundle = EvidenceBundle(url="https://test.com", overall_score=90)
    fv = FeatureVector()

    # AI Service MUST catch exception and return None gracefully
    summary = await service.generate_ai_summary(bundle, fv)
    assert summary is None
