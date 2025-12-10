from app.agent import get_llm
from app.agent.prompts import load_prompt_state, append_prompt_change


def generate_prompt_update(feedback_text: str, rating: int) -> str:
    model = get_llm()
    state = load_prompt_state()
    current_prompt = state["current_prompt"]

    prompt = (
        "Você é um assistente que ajusta prompts de sistema de um agente de IA.\n\n"
        f"Prompt atual:\n{current_prompt}\n\n"
        f"Feedback recebido (nota {rating}/5): {feedback_text}\n\n"
        "Sugira um NOVO prompt melhorado, em português, mantendo o objetivo original, "
        "mas incorporando as melhorias necessárias. Retorne APENAS o novo prompt."
    )

    resp = model.generate_content(prompt)
    return resp.text.strip()


def process_feedback(feedback_text: str, rating: int) -> str:
    new_prompt = generate_prompt_update(feedback_text, rating)
    description = f"Feedback (nota {rating}/5): {feedback_text}"
    append_prompt_change(description, new_prompt)
    return new_prompt