"""
SupportState — the shared state object that flows through the graph.
Every node receives this, optionally modifies it, and returns updates.
"""
from typing import Annotated, Literal, TypedDict
from langgraph.graph.message import add_messages


# Type alias for clarity
IntentType = Literal["billing", "technical", "general", "unknown"]


class SupportState(TypedDict):
    """
    State that flows through the support bot graph.
    
    Fields:
        messages: Full conversation history (auto-merged by add_messages).
        intent: Classified intent of the latest user message.
        confidence: Classifier's confidence score (0.0 to 1.0).
        requires_human: True if confidence is below threshold.
    """
    messages: Annotated[list, add_messages]
    intent: IntentType
    confidence: float
    requires_human: bool