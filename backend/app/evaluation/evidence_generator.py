"""
Evidence Generator.
Transforms EvaluationResult findings into explainable Evidence objects and bundles.
"""
from typing import List
from app.models.evaluation import EvaluationResult
from app.models.evidence import Evidence, EvidenceBundle


class EvidenceGenerator:
    """
    Constructs explainable evidence bundles from EvaluationResult.
    """

    @staticmethod
    def generate_bundle(url: str, evaluation_result: EvaluationResult) -> EvidenceBundle:
        failed_evidences: List[Evidence] = []
        passed_evidences: List[Evidence] = []

        for finding in evaluation_result.findings:
            evidence = Evidence(
                issue=finding.policy_name,
                category=finding.category,
                severity=finding.severity,
                observed_value=finding.observed_value,
                expected_value=finding.expected_value,
                recommendation=finding.recommendation
            )

            if finding.passed:
                passed_evidences.append(evidence)
            else:
                failed_evidences.append(evidence)

        return EvidenceBundle(
            url=url,
            overall_score=evaluation_result.overall_score,
            failed_evidences=failed_evidences,
            passed_evidences=passed_evidences
        )
