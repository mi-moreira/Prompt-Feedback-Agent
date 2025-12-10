from functools import lru_cache
import os
import google.generativeai as genai


@lru_cache(maxsize=1)
def get_llm():
    """Return a configured Gemini model instance."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    # Default to an available model ID; can be overridden via GEMINI_MODEL
    model_name = os.getenv("GEMINI_MODEL", "models/gemini-pro-latest")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)
