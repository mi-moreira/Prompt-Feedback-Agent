import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Avoid shadowing the real `app` package when this script is named app.py
_this_module = sys.modules.get(Path(__file__).stem)
if _this_module and getattr(_this_module, "__file__", None) == __file__:
    sys.modules.pop(Path(__file__).stem, None)


import streamlit as st
from app.agent.agent import chat_with_agent
from app.feedback.feedback_engine import process_feedback
from app.agent.prompts import load_prompt_state

st.set_page_config(page_title="Morphia AI Chat", layout="wide")

if "history" not in st.session_state:
    st.session_state["history"] = []  # list of {"role": "user"|"assistant", "content": str}

st.title("Morphia – Technical Test: Chatbot with Intelligent Feedback")

tab_chat, tab_feedback = st.tabs(["💬 Chat", "🛠 Feedback & Prompt"])

with tab_chat:
    st.subheader("Chat with the agent")

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["history"]:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Agent:** {msg['content']}")

    st.divider()

    user_input = st.text_area("Your message", key="chat_input", height=100)
    send = st.button("Send", type="primary")

    if send and user_input.strip():
        st.session_state["history"].append(
            {"role": "user", "content": user_input.strip()}
        )
        with st.spinner("Agent is thinking..."):
            answer = chat_with_agent(user_input.strip())
        st.session_state["history"].append(
            {"role": "assistant", "content": answer}
        )
        st.rerun()

with tab_feedback:
    st.subheader("Feedback about the agent's answers")

    st.markdown(
        "Rate the quality of the answers and help improve the **system prompt** that guides the agent."
    )

    rating = st.slider("Overall rating (1 = poor, 5 = excellent)", min_value=1, max_value=5, value=4)
    feedback_text = st.text_area(
        "Detailed feedback (what could be better? what was missing?)",
        height=120,
        key="feedback_text",
    )

    if st.button("Send feedback and update prompt"):
        if feedback_text.strip():
            with st.spinner("Updating prompt based on feedback..."):
                new_prompt = process_feedback(feedback_text.strip(), rating)
            st.success("Prompt updated successfully!")
            st.markdown("### New current prompt:")
            st.code(new_prompt, language="markdown")
        else:
            st.warning("Please write some feedback before sending.")

    st.divider()
    st.markdown("### Current prompt & history")
    state = load_prompt_state()
    st.markdown("**Current prompt:**")
    st.code(state["current_prompt"], language="markdown")

    with st.expander("View full prompt change history"):
        for item in reversed(state["history"]):
            st.markdown(f"- `{item['timestamp']}` – {item['change']}")
