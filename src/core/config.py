"""Centralized configuration loader with validation."""
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from src.core.exceptions import ConfigurationError

load_dotenv()


class Settings(BaseModel):
    groq_api_key: str = Field(..., description="Groq API key")
    llm_model: str = Field(default="llama-3.1-8b-instant")
    llm_temperature: float = Field(default=0.1, ge=0.0, le=1.0)
    confidence_threshold: float = Field(default=0.6, ge=0.0, le=1.0)
    
    @field_validator("groq_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v or not v.startswith("gsk_"):
            raise ConfigurationError(
                "GROQ_API_KEY is missing or invalid. "
                "Get one at https://console.groq.com/keys"
            )
        return v
    
    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            llm_model=os.getenv("LLM_MODEL", "llama-3.1-8b-instant"),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
            confidence_threshold=float(os.getenv("CONFIDENCE_THRESHOLD", "0.6")),
        )


settings = Settings.from_env()