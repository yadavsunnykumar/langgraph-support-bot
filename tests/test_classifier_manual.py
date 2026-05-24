"""
Quick manual smoke test — run before committing.
Not a real pytest test (we'll write those in Issue #9).
"""
from langchain_core.messages import HumanMessage
from src.agents.classifier import classifier_node


def main():
    test_cases = [
        "I was charged twice last month, please help",
        "The app keeps crashing when I click Login",
        "What are your business hours?",
        "hello",
    ]
    
    for query in test_cases:
        print(f"\n📩 Query: {query}")
        fake_state = {
            "messages": [HumanMessage(content=query)],
            "intent": "unknown",
            "confidence": 0.0,
            "requires_human": False,
        }
        result = classifier_node(fake_state)
        print(f"   → {result}")


if __name__ == "__main__":
    main()