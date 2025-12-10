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
if "last_answer" not in st.session_state:
    st.session_state["last_answer"] = ""

st.title("Morphia – Technical Test: Chatbot with Intelligent Feedback")

tab_chat, tab_feedback = st.tabs(["💬 Chat", "🛠 Feedback & Prompt"])

with tab_chat:
    col_title, col_actions = st.columns([0.8, 0.2])
    with col_title:
        st.subheader("Chat with the agent")
    with col_actions:
        if st.button("🧹 Clear chat", use_container_width=True):
            st.session_state["history"] = []
            st.session_state["last_answer"] = ""
            st.rerun()

    # Show current prompt collapsed for transparency
    with st.expander("Current system prompt"):
        st.text_area(
            "Prompt",
            load_prompt_state()["current_prompt"],
            height=180,
            key="current_prompt_view_chat",
        )

    # Quick prompt suggestions
    st.markdown("Try one:")
    cols = st.columns(3)
    quick_prompts = [
        "Me ajude a melhorar a descrição do meu estúdio de tatuagem.",
        "Sugira um script de vendas para novos clientes.",
        "Como organizar agenda e follow-up de orçamentos?",
    ]
    for i, qp in enumerate(quick_prompts):
        if cols[i].button(qp):
            st.session_state["history"].append({"role": "user", "content": qp})
            with st.spinner("Agent is thinking..."):
                answer = chat_with_agent(qp)
            st.session_state["history"].append({"role": "assistant", "content": answer})
            st.session_state["last_answer"] = answer
            st.rerun()

    # Render conversation using chat bubbles
    for msg in st.session_state["history"]:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])

    # Chat input with submit on Enter
    user_input = st.chat_input("Pergunte algo...", key="chat_input")
    if user_input:
        st.session_state["history"].append({"role": "user", "content": user_input.strip()})
        with st.spinner("Agent is thinking..."):
            answer = chat_with_agent(user_input.strip())
        st.session_state["history"].append({"role": "assistant", "content": answer})
        st.session_state["last_answer"] = answer
        st.rerun()

with tab_feedback:
    st.subheader("Feedback about the agent's answers")

    st.markdown(
        "Rate the quality of the answers and help improve the **system prompt** that guides the agent."
    )

    rating = st.slider("Overall rating (1 = poor, 5 = excellent)", min_value=1, max_value=5, value=4)
    last_answer = st.session_state.get("last_answer", "")
    prefill = f"Última resposta do agente:\n\"{last_answer}\"" if last_answer else ""
    feedback_text = st.text_area(
        "Detailed feedback (what could be better? what was missing?)",
        height=150,
        key="feedback_text",
        value=prefill,
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
    st.text_area(
        "Current prompt:",
        state["current_prompt"],
        height=220,
        key="current_prompt_view_feedback",
    )

    with st.expander("View full prompt change history"):
        for item in reversed(state["history"]):
            st.markdown(f"- `{item['timestamp']}` – {item['change']}")
