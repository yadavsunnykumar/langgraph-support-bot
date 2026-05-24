"""
Technical support agent — handles bugs, errors, how-to questions.
"""
from langchain_core.messages import AIMessage, SystemMessage
from src.core.llm import get_llm
from src.core.logger import logger
from src.graph.state import SupportState


TECHNICAL_SYSTEM_PROMPT = """You are a Technical Support Specialist for a SaaS product.

Your responsibilities:
- Troubleshoot bugs, errors, login issues, and feature problems
- Walk users through fixes step-by-step
- Ask clarifying questions: browser, device, error messages, when it started
- For complex bugs, collect details and mention an engineer will follow up

Guidelines:
- Use numbered steps for instructions
- Be specific and avoid jargon
- If you don't know, say so — never invent technical answers
- Suggest checking status page (status.company.com) for known outages

You do NOT handle billing or general inquiries.
"""


def technical_agent_node(state: SupportState) -> dict:
    """Generates a response for technical queries."""
    logger.info("→ Entering technical_agent_node")
    
    llm = get_llm(temperature=0.2)  # lower temp for accuracy
    
    messages = [SystemMessage(content=TECHNICAL_SYSTEM_PROMPT)] + state["messages"]
    
    try:
        response = llm.invoke(messages)
        logger.info(f"✓ Technical agent responded ({len(response.content)} chars)")
        
        return {"messages": [AIMessage(content=response.content)]}
    
    except Exception as e:
        logger.error(f"Technical agent failed: {e}")
        return {
            "messages": [AIMessage(
                content="I'm having trouble accessing technical resources right now. "
                        "Please try again or email support@company.com."
            )]
        }