"""
Intent classifier node.
Uses structured output to reliably extract intent + confidence.
"""
from pydantic import BaseModel, Field
from typing import Literal
from src.core.llm import get_llm
from src.core.logger import logger
from src.graph.state import SupportState


class IntentClassification(BaseModel):
    """Structured output schema for the classifier."""
    intent: Literal["billing", "technical", "general"] = Field(
        description="The category of the user's query."
    )
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Confidence score between 0 and 1."
    )
    reasoning: str = Field(
        description="One-sentence explanation of the classification."
    )


CLASSIFIER_PROMPT = """You are an intent classifier for a customer support system.

Classify the user's message into ONE of these categories:

- **billing**: Payments, invoices, refunds, subscriptions, pricing, charges
- **technical**: Bugs, errors, login issues, app crashes, how-to questions about features
- **general**: Greetings, company info, business hours, general inquiries

Provide:
1. The intent category
2. A confidence score (0.0 to 1.0) — be honest, use lower scores for ambiguous queries
3. Brief reasoning

User message: "{user_message}"
"""

# Confidence threshold — below this, escalate to human
CONFIDENCE_THRESHOLD = 0.6


def classifier_node(state: SupportState) -> dict:
    """
    Classifies the latest user message and updates the state.
    
    Returns a partial state update (LangGraph merges it automatically).
    """
    logger.info("→ Entering classifier_node")
    
    # Get the latest user message
    last_message = state["messages"][-1]
    user_text = last_message.content if hasattr(last_message, "content") else str(last_message)
    
    # Build structured-output LLM
    llm = get_llm(temperature=0.0)  # deterministic for classification
    structured_llm = llm.with_structured_output(IntentClassification)
    
    # Classify
    prompt = CLASSIFIER_PROMPT.format(user_message=user_text)
    
    try:
        result: IntentClassification = structured_llm.invoke(prompt)
        logger.info(
            f"✓ Classified as '{result.intent}' "
            f"(confidence={result.confidence:.2f}) — {result.reasoning}"
        )
        
        return {
            "intent": result.intent,
            "confidence": result.confidence,
            "requires_human": result.confidence < CONFIDENCE_THRESHOLD,
        }
    
    except Exception as e:
        logger.error(f"Classifier failed: {e}")
        # Graceful fallback — route to human
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "requires_human": True,
        }