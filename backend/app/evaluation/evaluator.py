"""
Evaluation Engine.
Evaluates FeatureVector against loaded PolicyRules with graduated penalty math.
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
    Evaluates observed feature metrics against policy rules with partial credit scoring.
    """

    # Category Weights for Overall Score Computation
    CATEGORY_WEIGHTS: Dict[Category, float] = {
        Category.SEO: 0.35,
        Category.PERFORMANCE: 0.25,
        Category.ACCESSIBILITY: 0.25,
        Category.CONTENT: 0.15,
    }

    def __init__(self, policies: List[PolicyRule]):
        self.policies = policies

    def evaluate(self, feature_vector: FeatureVector) -> EvaluationResult:
        findings: List[Finding] = []
        features_dict = feature_vector.model_dump()

        category_policy_scores: Dict[Category, List[float]] = {cat: [] for cat in Category}
        category_passed_counts: Dict[Category, int] = {cat: 0 for cat in Category}
        category_total_counts: Dict[Category, int] = {cat: 0 for cat in Category}

        for policy in self.policies:
            observed_val = features_dict.get(policy.feature)
            if observed_val is None:
                logger.warning(f"Feature '{policy.feature}' requested by policy '{policy.name}' not found in FeatureVector.")
                continue

            rule_score = self._compute_rule_score(policy, observed_val)
            passed = rule_score >= 0.85  # 85%+ score is considered passed

            category = policy.category
            category_total_counts[category] += 1
            category_policy_scores[category].append(rule_score)
            if passed:
                category_passed_counts[category] += 1

            finding = Finding(
                policy_name=policy.name,
                category=category,
                severity=policy.severity,
                observed_value=observed_val,
                expected_value=policy.expected_display,
                passed=passed,
                recommendation=policy.recommendation,
                weight=policy.weight
            )
            findings.append(finding)

        # Compute Category Scores
        category_scores: Dict[Category, CategoryScore] = {}
        for cat in Category:
            scores_list = category_policy_scores[cat]
            if scores_list:
                avg_ratio = sum(scores_list) / len(scores_list)
                cat_score_val = round(avg_ratio * 100)
            else:
                cat_score_val = 100

            category_scores[cat] = CategoryScore(
                category=cat,
                score=cat_score_val,
                passed_count=category_passed_counts[cat],
                total_count=category_total_counts[cat]
            )

        # Compute Weighted Overall Score
        weighted_sum = sum(
            category_scores[cat].score * self.CATEGORY_WEIGHTS[cat]
            for cat in Category
        )
        overall_score = round(weighted_sum)

        logger.info(f"Graduated Evaluation complete. Overall Score: {overall_score}/100. Category scores: {category_scores}")

        return EvaluationResult(
            overall_score=overall_score,
            category_scores=category_scores,
            findings=findings
        )

    @staticmethod
    def _compute_rule_score(policy: PolicyRule, value: Any) -> float:
        """
        Computes a continuous score ratio between 0.0 and 1.0 for a rule.
        Supports partial credit for minor numerical bounds deviations.
        """
        if isinstance(value, (int, float)):
            # Min bound penalty check
            if policy.min_value is not None and value < policy.min_value:
                diff = policy.min_value - value
                # Slight variance gets partial credit
                span = policy.min_value if policy.min_value > 0 else 100
                ratio = max(0.0, 1.0 - (diff / span))
                return round(ratio, 2)

            # Max bound penalty check
            if policy.max_value is not None and value > policy.max_value:
                diff = value - policy.max_value
                # Example: Title 61 vs max 60 -> diff=1, span=60 -> 1 - 1/60 = 0.98 (98% partial credit!)
                span = policy.max_value if policy.max_value > 0 else 100
                ratio = max(0.0, 1.0 - (diff / span))
                return round(ratio, 2)

            return 1.0

        if policy.exact_value is not None:
            return 1.0 if value == policy.exact_value else 0.0

        if policy.allowed_values is not None:
            return 1.0 if value in policy.allowed_values else 0.0

        if policy.disallowed_values is not None:
            return 0.0 if value in policy.disallowed_values else 1.0

        return 1.0
