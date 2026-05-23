# Technical Design Document

## 1. Architecture Overview
LangGraph StateGraph with the following nodes:
- classifier_node: Detects intent (billing/technical/general)
- billing_agent: Handles billing queries
- technical_agent: Handles technical queries  
- general_agent: Handles general queries
- human_escalation_node: Flags low-confidence cases

## 2. State Schema
class SupportState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: Literal["billing", "technical", "general", "unknown"]
    confidence: float
    requires_human: bool

## 3. Graph Flow
START → classifier → [conditional] → {billing | technical | general | escalation} → END

## 4. Tech Stack
- Python 3.11+
- LangGraph 0.2.x
- LangChain Core
- Groq (free LLM) — llama-3.1-8b-instant
- Pydantic for validation
- Streamlit for UI
- pytest for testing
- python-dotenv for secrets

## 5. Folder Structure
support-bot/
├── docs/
├── src/
│   ├── agents/          # billing.py, technical.py, general.py
│   ├── graph/           # state.py, nodes.py, builder.py
│   ├── core/            # config.py, llm.py, logger.py
│   └── ui/              # streamlit_app.py
├── tests/
├── .env.example
├── requirements.txt
└── README.md

## 6. Key Design Decisions
- MemorySaver checkpointer for v1 (SQLite in v2)
- Pydantic for LLM structured output (intent classification)
- Centralized config via core/config.py
- Logger for all node entries/exits (observability)