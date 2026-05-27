"""Shared pytest fixtures."""
import pytest
from langchain_core.messages import HumanMessage


@pytest.fixture
def sample_state():
    """A minimal valid state for unit tests."""
    return {
        "messages": [HumanMessage(content="test message")],
        "intent": "unknown",
        "confidence": 0.0,
        "requires_human": False,
    }


@pytest.fixture
def billing_query_state():
    return {
        "messages": [HumanMessage(content="I want a refund for my last invoice.")],
        "intent": "unknown",
        "confidence": 0.0,
        "requires_human": False,
    }