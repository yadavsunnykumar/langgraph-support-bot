"""
Billing agent — handles payments, refunds, subscriptions, invoices.
"""
from langchain_core.messages import AIMessage, SystemMessage
from src.core.llm import get_llm
from src.core.logger import logger
from src.graph.state import SupportState


BILLING_SYSTEM_PROMPT = """You are a Billing Support Specialist for a SaaS company.

Your responsibilities:
- Help with payment issues, refunds, invoices, and subscriptions
- Explain pricing plans and charges clearly
- Be empathetic — billing issues are stressful for users
- If you need account details, ask politely for the user's email or account ID
- For refund requests above $100, mention that a human agent will review

Guidelines:
- Keep responses concise (2-4 sentences usually)
- Never make up policies; if unsure, say you'll connect them to a human
- End with a helpful next step

You do NOT handle technical bugs or general inquiries — those belong to other teams.
"""


def billing_agent_node(state: SupportState) -> dict:
    """Generates a response for billing-related queries."""
    logger.info("→ Entering billing_agent_node")
    
    llm = get_llm(temperature=0.3)  # slight creativity for natural tone
    
    messages = [SystemMessage(content=BILLING_SYSTEM_PROMPT)] + state["messages"]
    
    try:
        response = llm.invoke(messages)
        logger.info(f"✓ Billing agent responded ({len(response.content)} chars)")
        
        return {"messages": [AIMessage(content=response.content)]}
    
    except Exception as e:
        logger.error(f"Billing agent failed: {e}")
        return {
            "messages": [AIMessage(
                content="I'm having trouble processing your billing query right now. "
                        "Please try again in a moment or contact billing@company.com."
            )]
        }