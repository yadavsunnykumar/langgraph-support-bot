"""
Routing logic — decides which agent handles the query based on classifier output.
"""
from typing import Literal
from src.core.logger import logger
from src.graph.state import SupportState


def route_after_classification(
    state: SupportState
) -> Literal["billing_agent", "technical_agent", "general_agent", "human_escalation"]:
    """
    Conditional edge function: returns the name of the next node.
    
    Routing rules:
    1. If requires_human (low confidence or unknown intent) → escalate
    2. Otherwise, route based on intent
    """
    intent = state.get("intent", "unknown")
    requires_human = state.get("requires_human", False)
    
    if requires_human or intent == "unknown":
        logger.info(f"⤴ Routing to: human_escalation")
        return "human_escalation"
    
    route_map = {
        "billing": "billing_agent",
        "technical": "technical_agent",
        "general": "general_agent",
    }
    
    next_node = route_map.get(intent, "human_escalation")
    logger.info(f"⤴ Routing to: {next_node}")
    return next_node