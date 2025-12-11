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
st.markdown(
    """
    <style>
    /* Hide Streamlit default toolbar/menu for a cleaner UI */
    [data-testid="stToolbar"], #MainMenu, header {visibility: hidden;}

    /* Tighten top spacing and add chip styling */
    .top-row { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; margin: 4px 0 8px 0; }
    .title-row { margin: 6px 0 10px 0; }
    .chip-row { display: flex; gap: 8px; flex-wrap: wrap; }
    .chip-row .stButton button {
        border-radius: 999px;
        padding: 8px 12px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
        color: #e2e8f0;
        box-shadow: none;
    }
    .chip-row .stButton button:hover { border-color: rgba(255,255,255,0.25); }

    /* Divider before input */
    .input-divider { margin: 6px 0 10px 0; border-top: 1px solid rgba(255,255,255,0.08); }

    /* Compact clear button */
    .clear-btn button {
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 12px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: #e2e8f0;
        box-shadow: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "history" not in st.session_state:
    st.session_state["history"] = []  # list of {"role": "user"|"assistant", "content": str}
if "last_answer" not in st.session_state:
    st.session_state["last_answer"] = ""
if "ui_lang" not in st.session_state:
    st.session_state["ui_lang"] = "pt"

def t(key: str) -> str:
    texts = {
        "pt": {
            "title": "Morphia – Teste Técnico: Chatbot com Feedback Inteligente",
            "chat_tab": "💬 Chat",
            "feedback_tab": "🛠 Feedback & Prompt",
            "chat_header": "Converse com o agente",
            "clear_chat": "🧹 Limpar chat",
            "current_prompt": "Prompt do sistema (atual)",
            "try_one": "Experimente:",
            "tools_title": "Ferramentas que o agente pode usar",
            "tools_desc": "- ViaCEP: mencione um CEP (ex.: `CEP 01001000`).\n- Pokémon: mencione um nome (ex.: `pokemon pikachu`).",
            "chat_input": "Pergunte algo...",
            "feedback_header": "Feedback sobre as respostas",
            "feedback_sub": "Avalie a qualidade e ajude a melhorar o prompt do sistema.",
            "rating": "Nota geral (1 = ruim, 5 = excelente)",
            "feedback_label": "Feedback detalhado (o que melhorar?)",
            "send_feedback": "Enviar feedback e atualizar prompt",
            "prompt_section": "Prompt atual e histórico",
            "prompt_label": "Prompt atual:",
            "history_title": "Ver histórico completo de alterações",
        },
        "en": {
            "title": "Morphia – Technical Test: Chatbot with Intelligent Feedback",
            "chat_tab": "💬 Chat",
            "feedback_tab": "🛠 Feedback & Prompt",
            "chat_header": "Chat with the agent",
            "clear_chat": "🧹 Clear chat",
            "current_prompt": "Current system prompt",
            "try_one": "Try one:",
            "tools_title": "Tools the agent can use",
            "tools_desc": "- ViaCEP lookup: mention a CEP (e.g., `CEP 01001000`).\n- Pokémon info: mention a Pokémon name (e.g., `pokemon pikachu`).",
            "chat_input": "Ask something...",
            "feedback_header": "Feedback about the agent's answers",
            "feedback_sub": "Rate the quality and help improve the system prompt.",
            "rating": "Overall rating (1 = poor, 5 = excellent)",
            "feedback_label": "Detailed feedback (what could be better?)",
            "send_feedback": "Send feedback and update prompt",
            "prompt_section": "Current prompt & history",
            "prompt_label": "Current prompt:",
            "history_title": "View full prompt change history",
        },
    }
    return texts[st.session_state["ui_lang"]].get(key, key)

# Top controls and title
lang = st.radio("Language / Idioma", ["Português", "English"], horizontal=True, key="ui_lang_radio")
st.session_state["ui_lang"] = "pt" if lang == "Português" else "en"

st.title(t("title"))

tab_chat, tab_feedback = st.tabs([t("chat_tab"), t("feedback_tab")])

with tab_chat:
    st.subheader(t("chat_header"))

    # Show current prompt collapsed for transparency
    with st.expander(t("current_prompt")):
        st.text_area(
            "Prompt",
            load_prompt_state()["current_prompt"],
            height=180,
            key="current_prompt_view_chat",
        )

    # Quick prompt suggestions
    st.markdown(t("try_one"))
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

    # Tool hints so users know what the agent can do
    with st.expander(t("tools_title")):
        st.markdown(t("tools_desc"))

    # Render conversation using chat bubbles
    for msg in st.session_state["history"]:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])

    st.markdown('<div class="input-divider"></div>', unsafe_allow_html=True)
    st.caption("Mensagem")

    # Chat input with submit on Enter
    user_input = st.chat_input(t("chat_input"), key="chat_input")
    if user_input:
        st.session_state["history"].append({"role": "user", "content": user_input.strip()})
        with st.spinner("Agent is thinking..."):
            answer = chat_with_agent(user_input.strip())
        st.session_state["history"].append({"role": "assistant", "content": answer})
        st.session_state["last_answer"] = answer
        st.rerun()

    # Compact clear chat button below input
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button(t("clear_chat"), key="clear_chat_bottom"):
        st.session_state["history"] = []
        st.session_state["last_answer"] = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with tab_feedback:
    st.subheader(t("feedback_header"))

    st.markdown(t("feedback_sub"))

    rating = st.slider(t("rating"), min_value=1, max_value=5, value=4)
    last_answer = st.session_state.get("last_answer", "")
    prefill = f"Última resposta do agente:\n\"{last_answer}\"" if last_answer else ""
    feedback_text = st.text_area(
        t("feedback_label"),
        height=150,
        key="feedback_text",
        value=prefill,
    )

    if st.button(t("send_feedback")):
        if feedback_text.strip():
            with st.spinner("Updating prompt based on feedback..."):
                new_prompt = process_feedback(feedback_text.strip(), rating)
            st.success("Prompt updated successfully!")
            st.markdown("### New current prompt:")
            st.code(new_prompt, language="markdown")
        else:
            st.warning("Please write some feedback before sending.")

    st.divider()
    st.markdown(f"### {t('prompt_section')}")
    state = load_prompt_state()
    st.text_area(
        t("prompt_label"),
        state["current_prompt"],
        height=220,
        key="current_prompt_view_feedback",
    )

    with st.expander(t("history_title")):
        for item in reversed(state["history"]):
            st.markdown(f"- `{item['timestamp']}` – {item['change']}")
