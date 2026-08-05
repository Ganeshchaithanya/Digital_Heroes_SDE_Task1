"""
Prompt Builder Module.
Receives EvidenceBundle and deterministically formats an LLM prompt.
Instructs the LLM to speak in a natural, human, expert conversational tone in English.
Performs NO reasoning or metric calculation.
"""
import json
from app.models.evidence import EvidenceBundle


class PromptBuilder:
    """
    Assembles structured prompts for LLM execution using provided EvidenceBundle.
    """

    SYSTEM_ROLE = (
        "You are PAGEPULSE AI - a friendly, expert Senior Software Architect and Website Auditor.\n"
        "Speak to the user naturally like a knowledgeable human colleague having a real conversation in clear, engaging English.\n"
        "Avoid dry, robotic corporate template language. Write warm, insightful, person-to-person technical feedback.\n\n"
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
                "- executive_summary: A 2-3 sentence conversational executive summary speaking directly to the website owner/developer in a natural, human voice in clear English.\n"
                "- key_strengths: Array of strings highlighting what the website does great in friendly, natural English.\n"
                "- prioritized_issues: Array of strings explaining the key issues in order of priority like a human expert explaining to a peer.\n"
                "- action_plan: Array of practical, step-by-step developer recommendations in plain, helpful English."
            )
        }

        return json.dumps(user_content, indent=2)
