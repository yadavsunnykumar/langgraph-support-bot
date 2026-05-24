"""
General agent — handles greetings, FAQs, and miscellaneous queries.
"""
from langchain_core.messages import AIMessage, SystemMessage
from src.core.llm import get_llm
from src.core.logger import logger
from src.graph.state import SupportState


GENERAL_SYSTEM_PROMPT = """You are a Customer Support Representative for a SaaS company.

Your responsibilities:
- Greet users warmly
- Answer general questions about the company, hours, contact info
- Help users understand what kind of help they can get

Company info (use only this):
- Business hours: Mon-Fri, 9 AM - 6 PM IST
- Email: hello@company.com
- We help teams collaborate on projects with AI-powered tools.

Guidelines:
- Be friendly and conversational
- If the user has a billing or technical issue, redirect them by asking a clarifying question
- Keep responses short (1-3 sentences)

You do NOT handle billing or technical issues directly.
"""


def general_agent_node(state: SupportState) -> dict:
    """Generates a response for general queries."""
    logger.info("→ Entering general_agent_node")
    
    llm = get_llm(temperature=0.5)  # warmer tone
    
    messages = [SystemMessage(content=GENERAL_SYSTEM_PROMPT)] + state["messages"]
    
    try:
        response = llm.invoke(messages)
        logger.info(f"✓ General agent responded ({len(response.content)} chars)")
        
        return {"messages": [AIMessage(content=response.content)]}
    
    except Exception as e:
        logger.error(f"General agent failed: {e}")
        return {
            "messages": [AIMessage(
                content="Hi! I'm having a small hiccup right now. Could you try again?"
            )]
        }
    