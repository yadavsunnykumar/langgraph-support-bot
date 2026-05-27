"""Unit tests for the routing logic. Pure function — fast, no LLM calls."""
import pytest
from src.graph.router import route_after_classification


def test_route_billing():
    state = {"intent": "billing", "confidence": 0.9, "requires_human": False}
    assert route_after_classification(state) == "billing_agent"


def test_route_technical():
    state = {"intent": "technical", "confidence": 0.9, "requires_human": False}
    assert route_after_classification(state) == "technical_agent"


def test_route_general():
    state = {"intent": "general", "confidence": 0.9, "requires_human": False}
    assert route_after_classification(state) == "general_agent"


def test_route_low_confidence_escalates():
    state = {"intent": "billing", "confidence": 0.3, "requires_human": True}
    assert route_after_classification(state) == "human_escalation"


def test_route_unknown_intent_escalates():
    state = {"intent": "unknown", "confidence": 0.0, "requires_human": True}
    assert route_after_classification(state) == "human_escalation"


def test_route_missing_keys_safe_default():
    """Router should not crash on missing state keys."""
    state = {}
    result = route_after_classification(state)
    assert result == "human_escalation"