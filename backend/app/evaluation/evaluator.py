"""
Evaluation Engine.
Evaluates FeatureVector against loaded PolicyRules deterministically.
No AI.
"""
from typing import List, Dict, Any
from app.models.features import FeatureVector
from app.models.evaluation import Finding, CategoryScore, EvaluationResult
from app.policies.schema import PolicyRule
from app.shared.enums import Category
from app.observability.logger import logger


class EvaluationEngine:
    """
    Evaluates observed feature metrics against policy rules.
    """

    def __init__(self, policies: List[PolicyRule]):
        self.policies = policies

    def evaluate(self, feature_vector: FeatureVector) -> EvaluationResult:
        findings: List[Finding] = []
        features_dict = feature_vector.model_dump()

        category_totals: Dict[Category, int] = {cat: 0 for cat in Category}
        category_weights: Dict[Category, int] = {cat: 0 for cat in Category}
        category_earned_weights: Dict[Category, int] = {cat: 0 for cat in Category}
        category_passed_counts: Dict[Category, int] = {cat: 0 for cat in Category}

        for policy in self.policies:
            observed_val = features_dict.get(policy.feature)
            if observed_val is None:
                logger.warning(f"Feature '{policy.feature}' requested by policy '{policy.name}' not found in FeatureVector.")
                continue

            passed = self._check_pass(policy, observed_val)

            category = policy.category
            weight = policy.weight

            category_totals[category] += 1
            category_weights[category] += weight
            if passed:
                category_earned_weights[category] += weight
                category_passed_counts[category] += 1

            finding = Finding(
                policy_name=policy.name,
                category=category,
                severity=policy.severity,
                observed_value=observed_val,
                expected_value=policy.expected_display,
                passed=passed,
                recommendation=policy.recommendation,
                weight=weight
            )
            findings.append(finding)

        # Compute Category Scores & Overall Weighted Score
        category_scores: Dict[Category, CategoryScore] = {}
        total_possible_weights = 0
        total_earned_weights = 0

        for cat in Category:
            total_cnt = category_totals[cat]
            if total_cnt > 0:
                tot_weight = category_weights[cat]
                earned_weight = category_earned_weights[cat]
                score_val = round((earned_weight / tot_weight) * 100) if tot_weight > 0 else 100

                total_possible_weights += tot_weight
                total_earned_weights += earned_weight
            else:
                score_val = 100

            category_scores[cat] = CategoryScore(
                category=cat,
                score=score_val,
                passed_count=category_passed_counts[cat],
                total_count=total_cnt
            )

        overall_score = round((total_earned_weights / total_possible_weights) * 100) if total_possible_weights > 0 else 100

        logger.info(f"Evaluation complete. Overall Score: {overall_score}/100. Category scores: {category_scores}")

        return EvaluationResult(
            overall_score=overall_score,
            category_scores=category_scores,
            findings=findings
        )

    @staticmethod
    def _check_pass(policy: PolicyRule, value: Any) -> bool:
        if policy.min_value is not None and isinstance(value, (int, float)):
            if value < policy.min_value:
                return False
        if policy.max_value is not None and isinstance(value, (int, float)):
            if value > policy.max_value:
                return False
        if policy.exact_value is not None:
            if value != policy.exact_value:
                return False
        if policy.allowed_values is not None:
            if value not in policy.allowed_values:
                return False
        if policy.disallowed_values is not None:
            if value in policy.disallowed_values:
                return False
        return True
