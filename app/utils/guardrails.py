def apply_guardrails(text: str) -> str:
    """
    Minimal guardrail stub to keep the response safe/usable.
    Extend with proper moderation if needed.
    """
    if not text or not text.strip():
        return "Não consegui gerar uma resposta agora. Tente novamente em instantes."
    return text.strip()
