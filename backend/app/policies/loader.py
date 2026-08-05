"""
Policy loader and registry with schema validation.
"""
import json
from pathlib import Path
from typing import List
from app.policies.schema import PolicyRule
from app.shared.exceptions import PolicyValidationError
from app.observability.logger import logger


class PolicyLoader:
    def __init__(self, version: str = "v1"):
        self.version = version
        self.policies_dir = Path(__file__).parent / version

    def load_policies(self) -> List[PolicyRule]:
        if not self.policies_dir.exists() or not self.policies_dir.is_dir():
            raise PolicyValidationError(f"Policies directory not found: {self.policies_dir}")

        policies: List[PolicyRule] = []
        for json_file in sorted(self.policies_dir.glob("*.json")):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                rule = PolicyRule.model_validate(data)
                policies.append(rule)
            except Exception as e:
                logger.error(f"Failed to load policy JSON file '{json_file.name}': {e}")
                raise PolicyValidationError(
                    message=f"Invalid policy schema in file {json_file.name}: {str(e)}",
                    details={"file": json_file.name, "error": str(e)}
                ) from e

        logger.info(f"Successfully loaded {len(policies)} policies from '{self.version}'")
        return policies
