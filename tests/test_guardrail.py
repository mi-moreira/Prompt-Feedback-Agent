from app.utils.guardrails import apply_guardrails


def test_redacts_and_truncates():
    txt = "Here is a key: AIzaSyABCDEF123456789 and an email test@example.com " + ("x" * 2100)
    out = apply_guardrails(txt)
    assert "[REDACTED_GOOGLE_KEY]" in out
    assert "[REDACTED_EMAIL]" in out
    assert len(out) < len(txt)
