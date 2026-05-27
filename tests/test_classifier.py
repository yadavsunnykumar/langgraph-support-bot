"""Unit tests for the classifier node."""
import pytest
from langchain_core.messages import HumanMessage
from src.agents.classifier import classifier_node


@pytest.mark.parametrize("query,expected_intent", [
    ("I was charged twice this month", "billing"),
    ("Refund my last payment please", "billing"),
    ("My subscription auto-renewed by mistake", "billing"),
    ("The app crashes when I click save", "technical"),
    ("I can't log in, getting a 500 error", "technical"),
    ("How do I export my data?", "technical"),
    ("Hello!", "general"),
    ("What are your business hours?", "general"),
])
def test_classifier_correct_intent(query, expected_intent):
    """Classifier should correctly identify intent for clear queries."""
    state = {
        "messages": [HumanMessage(content=query)],
        "intent": "unknown",
        "confidence": 0.0,
        "requires_human": False,
    }
    
    result = classifier_node(state)
    
    assert result["intent"] == expected_intent, (
        f"Expected '{expected_intent}' for query '{query}', got '{result['intent']}'"
    )
    assert 0.0 <= result["confidence"] <= 1.0


def test_classifier_returns_required_keys(sample_state):
    """Classifier output must contain all required state keys."""
    result = classifier_node(sample_state)
    
    assert "intent" in result
    assert "confidence" in result
    assert "requires_human" in result


def test_classifier_low_confidence_escalates():
    """Ambiguous queries should have lower confidence and trigger escalation."""
    state = {
        "messages": [HumanMessage(content="asdfgh qwerty 12345")],
        "intent": "unknown",
        "confidence": 0.0,
        "requires_human": False,
    }
    
    result = classifier_node(state)
    
    # Either flagged for human OR returned unknown intent
    assert result["requires_human"] is True or result["intent"] == "unknown"