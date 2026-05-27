"""
Conversation service — the public API for running conversations.
Abstracts away graph internals so UI/tests don't depend on LangGraph directly.
"""
from typing import Optional
from langchain_core.messages import HumanMessage
from src.graph.builder import support_graph
from src.core.logger import logger


class ConversationService:
    """
    Handles multi-turn conversations with persistent memory per thread.
    
    Usage:
        service = ConversationService()
        reply = service.send_message("Hi there", thread_id="user-123")
        reply = service.send_message("I have a billing issue", thread_id="user-123")
        # Second call remembers the first.
    """
    
    def __init__(self):
        self.graph = support_graph
    
    def send_message(self, user_message: str, thread_id: str) -> dict:
        """
        Sends a user message and returns the bot's response + metadata.
        
        Args:
            user_message: The user's text input.
            thread_id: Unique conversation ID (persists context).
        
        Returns:
            dict with keys: reply, intent, confidence, requires_human
        """
        logger.info(f"💬 Thread '{thread_id}': received message")
        
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            result = self.graph.invoke(
                {"messages": [HumanMessage(content=user_message)]},
                config=config,
            )
            
            last_message = result["messages"][-1]
            
            return {
                "reply": last_message.content,
                "intent": result.get("intent", "unknown"),
                "confidence": result.get("confidence", 0.0),
                "requires_human": result.get("requires_human", False),
            }
        
        except Exception as e:
            logger.exception(f"Conversation service failed for thread '{thread_id}'")
            return {
                "reply": "Sorry, something went wrong. Please try again.",
                "intent": "unknown",
                "confidence": 0.0,
                "requires_human": True,
                "error": str(e),
            }
    
    def get_conversation_history(self, thread_id: str) -> list:
        """Retrieves the full message history for a thread."""
        config = {"configurable": {"thread_id": thread_id}}
        state = self.graph.get_state(config)
        
        if state and state.values:
            return state.values.get("messages", [])
        return []
    
    def reset_conversation(self, thread_id: str) -> None:
        """Clears conversation memory for a thread (for v1: just logs intent)."""
        # Note: MemorySaver doesn't have a public delete API in 0.2.x.
        # For v1, we just use a new thread_id. For v2 (SQLite), we'd DELETE.
        logger.info(f"🔄 Reset requested for thread '{thread_id}' (start new thread_id)")


# Module-level singleton
conversation_service = ConversationService()