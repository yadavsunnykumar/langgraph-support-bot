"""
Manual smoke test for the full graph.
Runs 4 different queries through the entire workflow.
"""
from langchain_core.messages import HumanMessage
from src.graph.builder import support_graph


def run_query(query: str, thread_id: str = "test-thread-1"):
    """Runs a single query through the graph and prints the result."""
    print(f"\n{'='*60}")
    print(f"📩 USER: {query}")
    print(f"{'='*60}")
    
    config = {"configurable": {"thread_id": thread_id}}
    
    result = support_graph.invoke(
        {"messages": [HumanMessage(content=query)]},
        config=config,
    )
    
    print(f"🎯 Intent: {result.get('intent')} (confidence: {result.get('confidence', 0):.2f})")
    print(f"👤 Escalated: {result.get('requires_human')}")
    print(f"🤖 BOT: {result['messages'][-1].content}")


def main():
    test_cases = [
        ("I was charged twice for my subscription this month!", "user-1"),
        ("My app crashes every time I open the dashboard", "user-2"),
        ("Hi! What are your business hours?", "user-3"),
        ("asdf qwerty 1234", "user-4"),  # gibberish → should escalate
    ]
    print(support_graph.get_graph().draw_mermaid())
    
    for query, thread in test_cases:
        run_query(query, thread)


if __name__ == "__main__":
    main()