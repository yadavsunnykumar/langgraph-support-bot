"""
Centralized configuration loader.
Loads environment variables and exposes them as typed settings.
"""
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    """Application settings loaded from environment variables."""
    
    groq_api_key: str = Field(..., description="Groq API key")
    llm_model: str = Field(default="llama-3.1-8b-instant")
    llm_temperature: float = Field(default=0.1, ge=0.0, le=1.0)
    
    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            llm_model=os.getenv("LLM_MODEL", "llama-3.1-8b-instant"),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
        )


# Singleton instance — import this anywhere
settings = Settings.from_env()