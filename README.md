# 🤖 Smart Customer Support Bot

A production-ready, multi-agent customer support system built with **LangGraph**.
Classifies incoming queries by intent and routes them to specialized agents
(Billing, Technical, General) with confidence-based human escalation.

![Demo](docs/demo.gif)

---

## ✨ Features

- 🎯 **Intent classification** with structured output and confidence scoring
- 🔀 **Conditional routing** to 3 specialized agents via LangGraph
- 👤 **Human-in-the-loop escalation** when confidence is low
- 💾 **Persistent conversation memory** with thread-based checkpointing
- 🧱 **Clean architecture** — service layer separates UI from graph logic
- ✅ **Unit + integration tests** with pytest
- 📊 **Observable** — structured logging, routing transparency in UI
- 🛡️ **Graceful error handling** at every node

---

## 🏗️ Architecture

┌─────────┐
│ START │
└────┬────┘
│
▼
┌──────────────┐
│ Classifier │ ── Pydantic structured output
└──────┬───────┘
│ conditional routing
│
┌───┴────┬────────┬──────────┐
▼ ▼ ▼ ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌─────────────┐
│Billing │ │Technical│ │General │ │ Human │
│ Agent │ │ Agent │ │ Agent │ │ Escalation │
└───┬────┘ └───┬────┘ └───┬────┘ └─────┬───────┘
│ │ │ │
└──────────┴──────────┴─────────────┘
│
▼
┌─────┐
│ END │
└─────┘

See [architecture diagram](docs/architecture.png) for the full Mermaid graph.

---

## 🚀 Quickstart

### Prerequisites

- Python 3.11+
- A free Groq API key — [get one here](https://console.groq.com/keys)

### Setup

```bash
# Clone
git clone https://github.com/<your-username>/langgraph-support-bot.git
cd langgraph-support-bot

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
make install
# or: pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Run

```bash
make run
# or: streamlit run src/ui/streamlit_app.py
```

Open http://localhost:8501 in your browser.

---

## 🧪 Testing

```bash
make test-fast     # unit tests only (no LLM calls)
make test          # full suite (unit + integration)
```

---

## 📁 Project Structure

support-bot/
├── docs/ # PRD, technical design, diagrams
├── src/
│ ├── agents/ # Specialist agents (billing, technical, general, escalation)
│ ├── core/ # Config, logger, LLM factory, exceptions
│ ├── graph/ # State schema, router, graph builder
│ ├── services/ # Conversation service (public API)
│ └── ui/ # Streamlit interface
├── tests/ # Unit + integration tests
├── Makefile # Common dev tasks
├── requirements.txt
└── README.md

---

## 🎓 Key Design Decisions

| Decision                                          | Rationale                                                         |
| ------------------------------------------------- | ----------------------------------------------------------------- |
| **Service layer** between UI and graph            | UI doesn't depend on LangGraph internals; easier to test and swap |
| **Pydantic structured output** for classification | Far more reliable than parsing raw LLM text                       |
| **Confidence threshold** for escalation           | Uncertain queries go to humans — real product behavior            |
| **Singleton compiled graph**                      | Compile once at import, not per request — major perf win          |
| **Different temperatures per agent**              | Billing/technical need accuracy (0.2), general can be warm (0.5)  |
| **Try/except with fallback messages**             | Graph never crashes — degrades gracefully                         |

---

## 🛠️ Tech Stack

- **LangGraph** — agent orchestration
- **LangChain** — LLM abstractions
- **Groq** (Llama 3.1 8B) — fast, free LLM inference
- **Pydantic** — structured output and config validation
- **Streamlit** — chat UI
- **pytest** — testing
- **loguru** — structured logging

---

## 📈 What's Next (v2)

- [ ] Swap MemorySaver → SQLite checkpointer for persistent threads across restarts
- [ ] Add tool calling — billing agent queries a real database
- [ ] Integration with Zendesk for ticket creation on escalation
- [ ] Multi-language support
- [ ] Latency + cost dashboards

---

## 📄 License

MIT
