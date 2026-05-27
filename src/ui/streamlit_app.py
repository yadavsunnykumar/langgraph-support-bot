"""
Streamlit chat interface for the Support Bot.
Run with: streamlit run src/ui/streamlit_app.py
"""
import uuid
import streamlit as st
from src.services.conversation import conversation_service


# ─── Page Setup ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Support Bot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Smart Customer Support Bot")
st.caption("Powered by LangGraph • Multi-agent routing • Built with Groq")


# ─── Session State ──────────────────────────────────────────────────
if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"streamlit-{uuid.uuid4().hex[:8]}"

if "messages" not in st.session_state:
    st.session_state.messages = []


# ─── Sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Session Info")
    st.code(st.session_state.thread_id, language=None)
    
    if st.button("🔄 New Conversation"):
        st.session_state.thread_id = f"streamlit-{uuid.uuid4().hex[:8]}"
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("Try these:")
    st.markdown("""
    - *"I was charged twice for my subscription"*
    - *"The app crashes when I click save"*
    - *"What are your business hours?"*
    - *"Hi there!"*
    """)
    
    st.divider()
    st.caption("Built with LangGraph + Groq")


# ─── Chat History ───────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("metadata"):
            with st.expander("🔍 Routing details"):
                meta = msg["metadata"]
                col1, col2, col3 = st.columns(3)
                col1.metric("Intent", meta["intent"])
                col2.metric("Confidence", f"{meta['confidence']:.2f}")
                col3.metric("Escalated", "Yes" if meta["requires_human"] else "No")


# ─── Chat Input ─────────────────────────────────────────────────────
if user_input := st.chat_input("How can I help you today?"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversation_service.send_message(
                user_input, st.session_state.thread_id
            )
        
        st.write(response["reply"])
        
        with st.expander("🔍 Routing details"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Intent", response["intent"])
            col2.metric("Confidence", f"{response['confidence']:.2f}")
            col3.metric("Escalated", "Yes" if response["requires_human"] else "No")
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["reply"],
        "metadata": {
            "intent": response["intent"],
            "confidence": response["confidence"],
            "requires_human": response["requires_human"],
        },
    })
    