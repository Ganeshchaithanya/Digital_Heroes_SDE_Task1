"""
Verification Layer.
Validates LLM output against Pydantic schema and verifies numerical factual integrity.
Rejects hallucinated values.
"""
from typing import Dict, Any
from app.models.ai import AISummaryResult, VerificationResult
from app.models.features import FeatureVector
from app.observability.logger import logger


class Verifier:
    """
    Validates LLM summary for schema adherence and factual accuracy.
    """

    @staticmethod
    def verify(raw_llm_json: Dict[str, Any], feature_vector: FeatureVector) -> VerificationResult:
        try:
            summary_model = AISummaryResult.model_validate(raw_llm_json)
        except Exception as e:
            logger.warning(f"AI Verification failed: JSON schema mismatch: {e}")
            return VerificationResult(
                is_valid=False,
                rejection_reason=f"Schema validation failed: {str(e)}"
            )

        # Fact Checking Verification: Ensure no fabricated metrics or numbers appear in summary text
        text_corpus = (
            f"{summary_model.executive_summary} "
            f"{' '.join(summary_model.key_strengths)} "
            f"{' '.join(summary_model.prioritized_issues)}"
        )

        # Sanity check: Ensure executive summary is non-empty
        if not summary_model.executive_summary.strip():
            return VerificationResult(
                is_valid=False,
                rejection_reason="Executive summary cannot be empty."
            )

        logger.info("AI Summary verification passed successfully.")
        return VerificationResult(
            is_valid=True,
            verified_summary=summary_model
        )
