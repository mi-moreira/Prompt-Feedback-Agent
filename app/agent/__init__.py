import os
import google.generativeai as genai

GEMINI_MODEL_NAME = "gemini-pro-latest"


def configure_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(GEMINI_MODEL_NAME)


_llm_model = None


def get_llm():
    global _llm_model
    if _llm_model is None:
        _llm_model = configure_llm()
    return _llm_model