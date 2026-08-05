"""
App settings and configuration using Pydantic Settings.
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "PAGEPULSE"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Groq AI Settings
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    
    # Inspection Engine Settings
    HTTP_TIMEOUT_SECONDS: float = 10.0
    MAX_REDIRECTS: int = 5
    USER_AGENT: str = "PagePulse-Inspection-Bot/1.0 (+https://pagepulse.app)"
    
    # Policies Directory
    POLICIES_VERSION: str = "v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
