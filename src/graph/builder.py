"""
Graph builder — assembles all nodes and edges into the final compiled graph.
This is the entry point everyone (UI, tests) imports.
"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.graph.state import SupportState
from src.graph.router import route_after_classification

from src.agents.classifier import classifier_node
from src.agents.billing import billing_agent_node
from src.agents.technical import technical_agent_node
from src.agents.general import general_agent_node
from src.agents.escalation import human_escalation_node

from src.core.logger import logger


def build_support_graph():
    """
    Builds and compiles the support bot graph.
    
    Flow:
        START → classifier → [conditional routing] → {billing | technical | general | escalation} → END
    
    Returns:
        Compiled graph with in-memory checkpointer for conversation persistence.
    """
    logger.info("🔧 Building support graph...")
    
    workflow = StateGraph(SupportState)
    
    # Register all nodes
    workflow.add_node("classifier", classifier_node)
    workflow.add_node("billing_agent", billing_agent_node)
    workflow.add_node("technical_agent", technical_agent_node)
    workflow.add_node("general_agent", general_agent_node)
    workflow.add_node("human_escalation", human_escalation_node)
    
    # Entry point: always start with classification
    workflow.add_edge(START, "classifier")
    
    # Conditional routing from classifier
    workflow.add_conditional_edges(
        "classifier",
        route_after_classification,
        {
            "billing_agent": "billing_agent",
            "technical_agent": "technical_agent",
            "general_agent": "general_agent",
            "human_escalation": "human_escalation",
        },
    )
    
    # All terminal nodes → END
    workflow.add_edge("billing_agent", END)
    workflow.add_edge("technical_agent", END)
    workflow.add_edge("general_agent", END)
    workflow.add_edge("human_escalation", END)
    
    # Checkpointer for conversation memory (we'll use this fully in Issue #8)
    checkpointer = MemorySaver()
    
    graph = workflow.compile(checkpointer=checkpointer)
    
    logger.info("✓ Support graph compiled successfully")
    return graph


# Singleton — build once at import
support_graph = build_support_graph()