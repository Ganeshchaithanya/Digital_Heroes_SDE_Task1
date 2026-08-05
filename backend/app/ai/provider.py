"""
Groq API Provider Module.
Executes asynchronous HTTP requests to Groq OpenAI-compatible Chat Completions endpoint.
"""
import json
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
from app.shared.exceptions import AIServiceError
from app.observability.logger import logger


class GroqProvider:
    """
    Client for Groq LLM API.
    """

    def __init__(
        self,
        api_key: Optional[str] = settings.GROQ_API_KEY,
        model: str = settings.GROQ_MODEL,
        api_url: str = settings.GROQ_API_URL
    ):
        self.api_key = api_key
        self.model = model
        self.api_url = api_url

    async def generate_summary(self, system_role: str, user_prompt: str) -> Dict[str, Any]:
        if not self.api_key:
            raise AIServiceError("Groq API key is not configured in environment variables.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_role},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(self.api_url, headers=headers, json=payload)
                
                if response.status_code != 200:
                    logger.error(f"Groq API returned HTTP {response.status_code}: {response.text}")
                    raise AIServiceError(f"Groq API error status {response.status_code}")

                data = response.json()
                content = data["choices"][0]["message"]["content"]
                parsed_json = json.loads(content)
                return parsed_json

        except httpx.RequestError as e:
            logger.error(f"Network error communicating with Groq API: {e}")
            raise AIServiceError(f"Groq API network error: {str(e)}") from e
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Groq response JSON: {e}")
            raise AIServiceError("Invalid JSON returned by Groq API.") from e
        except Exception as e:
            logger.error(f"Unexpected error in Groq provider: {e}")
            raise AIServiceError(f"Groq provider error: {str(e)}") from e
