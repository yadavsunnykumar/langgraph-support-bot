"""Manual test: verify conversation memory works across turns."""
from src.services.conversation import conversation_service


def main():
    thread = "memory-test-1"
    
    print("\n--- Turn 1 ---")
    r1 = conversation_service.send_message(
        "Hi, I'm Priya and I was double-charged.", thread
    )
    print(f"Bot: {r1['reply']}")
    
    print("\n--- Turn 2 ---")
    r2 = conversation_service.send_message(
        "Can you remind me what my name is?", thread
    )
    print(f"Bot: {r2['reply']}")
    
    print("\n--- Turn 3: different thread, no memory ---")
    r3 = conversation_service.send_message(
        "What's my name?", "different-thread"
    )
    print(f"Bot: {r3['reply']}")


if __name__ == "__main__":
    main()