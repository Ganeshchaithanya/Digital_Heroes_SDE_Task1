"""
AI Service Orchestrator.
Orchestrates PromptBuilder, GroqProvider, and Verifier.
Provides fail-safe catch block: AI failure NEVER breaks main application request.
"""
from typing import Optional
from app.models.evidence import EvidenceBundle
from app.models.features import FeatureVector
from app.models.ai import AISummaryResult
from app.ai.builder import PromptBuilder
from app.ai.provider import GroqProvider
from app.ai.verifier import Verifier
from app.observability.logger import logger


class AIService:
    """
    Optional AI Service wrapper with total fail-safe error handling.
    """

    def __init__(self, provider: Optional[GroqProvider] = None):
        self.provider = provider or GroqProvider()

    async def generate_ai_summary(
        self,
        evidence_bundle: EvidenceBundle,
        feature_vector: FeatureVector
    ) -> Optional[AISummaryResult]:
        try:
            logger.info("Executing AI Summary generation pipeline...")
            prompt = PromptBuilder.build_prompt(evidence_bundle)
            raw_response = await self.provider.generate_summary(
                system_role=PromptBuilder.SYSTEM_ROLE,
                user_prompt=prompt
            )
            verification = Verifier.verify(raw_response, feature_vector)

            if verification.is_valid and verification.verified_summary:
                logger.info("AI Summary successfully generated and verified.")
                return verification.verified_summary
            else:
                logger.warning(f"AI Summary rejected by verifier: {verification.rejection_reason}")
                return None

        except Exception as e:
            logger.warning(f"AI Service encountered an error (failing gracefully): {e}")
            return None
