"""
Prompt Builder Module.
Receives EvidenceBundle and deterministically formats an LLM prompt.
Performs NO reasoning or metric calculation.
"""
import json
from app.models.evidence import EvidenceBundle


class PromptBuilder:
    """
    Assembles structured prompts for LLM execution using provided EvidenceBundle.
    """

    SYSTEM_ROLE = (
        "You are PAGEPULSE AI - a Website Inspection Assistant.\n"
        "Your role is to summarize and explain website technical findings based STRICTLY on the provided evidence.\n"
        "STRICT RULES:\n"
        "1. Never invent or hallucinate metrics, issues, or numbers.\n"
        "2. Do not modify observed values or expected values.\n"
        "3. Only use supplied evidence.\n"
        "4. Output MUST be valid JSON adhering strictly to the required schema."
    )

    @classmethod
    def build_prompt(cls, evidence_bundle: EvidenceBundle) -> str:
        failed_issues = [
            {
                "issue": ev.issue,
                "category": ev.category.value,
                "severity": ev.severity.value,
                "observed_value": str(ev.observed_value),
                "expected_value": ev.expected_value,
                "recommendation": ev.recommendation
            }
            for ev in evidence_bundle.failed_evidences
        ]

        passed_items = [
            {
                "check": ev.issue,
                "category": ev.category.value,
                "observed_value": str(ev.observed_value)
            }
            for ev in evidence_bundle.passed_evidences
        ]

        user_content = {
            "website_url": evidence_bundle.url,
            "overall_score": evidence_bundle.overall_score,
            "failed_evidences": failed_issues,
            "passed_checks": passed_items,
            "instructions": (
                "Provide a JSON response with the following keys:\n"
                "- executive_summary: A concise 2-sentence summary of website health.\n"
                "- key_strengths: Array of strings describing passed checks.\n"
                "- prioritized_issues: Array of strings describing failed checks in order of severity.\n"
                "- action_plan: Array of concrete step-by-step developer recommendations."
            )
        }

        return json.dumps(user_content, indent=2)
