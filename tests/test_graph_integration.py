"""End-to-end integration tests. Uses real LLM — slower, but high signal."""
import pytest
from src.services.conversation import conversation_service


@pytest.mark.integration
def test_billing_query_routes_correctly():
    result = conversation_service.send_message(
        "I want a refund for my last subscription charge",
        thread_id="test-billing-1"
    )
    assert result["intent"] == "billing"
    assert len(result["reply"]) > 20


@pytest.mark.integration
def test_technical_query_routes_correctly():
    result = conversation_service.send_message(
        "The app keeps crashing when I open settings",
        thread_id="test-tech-1"
    )
    assert result["intent"] == "technical"
    assert len(result["reply"]) > 20


@pytest.mark.integration
def test_memory_persists_across_turns():
    thread = "test-memory-integration"
    
    conversation_service.send_message(
        "Hi, my account email is test@example.com", thread
    )
    result = conversation_service.send_message(
        "What email did I just give you?", thread
    )
    
    # Bot's reply should reference the email
    assert "test@example.com" in result["reply"].lower() or "@example.com" in result["reply"]