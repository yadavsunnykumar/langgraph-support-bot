"""
LLM factory — single source of truth for creating LLM clients.
If we ever switch providers, we change ONE file.
"""
from langchain_groq import ChatGroq
from src.core.config import settings
from src.core.logger import logger


def get_llm(temperature: float | None = None) -> ChatGroq:
    """
    Returns a configured Groq LLM client.
    
    Args:
        temperature: Optional override for sampling temperature.
    """
    temp = temperature if temperature is not None else settings.llm_temperature
    
    logger.debug(f"Initializing LLM: {settings.llm_model} (temp={temp})")
    
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.llm_model,
        temperature=temp,
    )