"""
Human escalation node — handles low-confidence queries and unknown intents.
In production, this would create a ticket in Zendesk/Intercom/etc.
"""
from langchain_core.messages import AIMessage
from src.core.logger import logger
from src.graph.state import SupportState


def human_escalation_node(state: SupportState) -> dict:
    """
    Escalates the conversation to a human agent.
    For v1: returns a polite message. For v2: would create a support ticket.
    """
    logger.warning(
        f"⚠ Escalating to human — intent={state.get('intent')} "
        f"confidence={state.get('confidence', 0):.2f}"
    )
    
    # In a real system, you'd call: ticket_service.create(state["messages"])
    # For now, just respond to the user.
    
    escalation_message = (
        "I want to make sure you get the best help possible, so I'm "
        "connecting you with one of our human support specialists. "
        "They'll reach out within 1 business hour. "
        "In the meantime, is there anything else I can help clarify?"
    )
    
    return {
        "messages": [AIMessage(content=escalation_message)],
        "requires_human": True,
    }