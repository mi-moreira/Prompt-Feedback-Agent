from pathlib import Path
from datetime import datetime
import json

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
PROMPT_FILE = DATA_DIR / "prompt_state.json"

DEFAULT_PROMPT = (
    "Você é um agente de IA da Morphia, que ajuda tatuadores e estúdios. "
    "Responda de forma objetiva, profissional e empática. "
    "Sempre explique seus passos quando usar ferramentas ou contexto externo. "
    "Evite inventar dados; se não souber, admita e sugira caminhos."
)


def _init_file_if_needed():
    if not PROMPT_FILE.exists():
        state = {
            "current_prompt": DEFAULT_PROMPT,
            "history": [
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "change": "Prompt inicial padrão definido.",
                }
            ],
        }
        PROMPT_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def load_prompt_state():
    _init_file_if_needed()
    return json.loads(PROMPT_FILE.read_text())


def save_prompt_state(state: dict):
    PROMPT_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def get_current_prompt() -> str:
    state = load_prompt_state()
    return state["current_prompt"]


def append_prompt_change(description: str, new_prompt: str | None = None):
    state = load_prompt_state()
    state["history"].append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "change": description,
            "new_prompt_snapshot": new_prompt or state["current_prompt"],
        }
    )
    if new_prompt:
        state["current_prompt"] = new_prompt
    save_prompt_state(state)