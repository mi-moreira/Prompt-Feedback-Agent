import re

SENSITIVE_PATTERNS = [
    # Common API key shapes
    (re.compile(r"AIza[0-9A-Za-z\-_]{10,}"), "[REDACTED_GOOGLE_KEY]"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "[REDACTED_KEY]"),
    # Basic email/phone cleanup
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "[REDACTED_EMAIL]"),
    (re.compile(r"\+?\d[\d\s().-]{8,}\d"), "[REDACTED_PHONE]"),
]

MAX_RESPONSE_CHARS = 2000


def apply_guardrails(text: str) -> str:
    """
    Lightweight guardrail to keep responses safe and readable.
    - Ensures non-empty text
    - Redacts obvious secrets/contact info
    - Trims overly long outputs
    Extend with proper moderation if needed.
    """
    if not text or not text.strip():
        return "Não consegui gerar uma resposta agora. Tente novamente em instantes."

    cleaned = text.strip()
    redacted = cleaned
    for pattern, replacement in SENSITIVE_PATTERNS:
        redacted = pattern.sub(replacement, redacted)

    truncated = redacted
    if len(truncated) > MAX_RESPONSE_CHARS:
        truncated = truncated[:MAX_RESPONSE_CHARS].rsplit(" ", 1)[0] + " …"

    if truncated != cleaned:
        return f"{truncated}\n\n[Alguns dados sensíveis ou muito longos foram filtrados.]"
    return truncated
