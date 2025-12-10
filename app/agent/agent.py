import re
from typing import List, Dict
from app import get_llm
from app.agent.prompts import get_current_prompt
from app.agent.tools import TOOLS_REGISTRY, ToolError
from app.vectorstore.store import retrieve_relevant_docs
from app.utils.guardrails import apply_guardrails
from app.utils.logging_utils import log_event


def build_system_message(query: str) -> str:
    base_prompt = get_current_prompt()
    docs = retrieve_relevant_docs(query, k=3)
    knowledge_block = "\n\n".join(f"- {d}" for d in docs)
    system = (
        f"{base_prompt}\n\n"
        f"Contexto relevante da base vetorial:\n{knowledge_block}\n\n"
        "Quando fizer suposições, deixe isso explícito."
    )
    return system


def tool_call(tool_name: str, arg: str) -> str:
    if tool_name not in TOOLS_REGISTRY:
        return f"Ferramenta desconhecida: {tool_name}"
    func = TOOLS_REGISTRY[tool_name]["func"]
    try:
        result = func(arg)
        return f"Resultado da ferramenta {tool_name}({arg}): {result}"
    except ToolError as e:
        return f"Erro ao usar {tool_name}: {e}"
    except Exception as e:
        return f"Erro inesperado ao usar {tool_name}: {e}"


def decide_tool_usage(user_message: str) -> List[Dict]:
    tools_to_use = []
    text = user_message.lower()
    if "cep" in text:
        match = re.search(r"\b(\d{8})\b", text)
        if match:
            tools_to_use.append({"name": "via_cep", "arg": match.group(1)})
    if "pokémon" in text or "pokemon" in text:
        name = text.split()[-1]
        tools_to_use.append({"name": "pokemon_info", "arg": name})
    return tools_to_use


def chat_with_agent(user_message: str) -> str:
    log_event("user_message", message=user_message)
    model = get_llm()

    system_msg = build_system_message(user_message)

    tool_results = []
    for t in decide_tool_usage(user_message):
        res = tool_call(t["name"], t["arg"])
        tool_results.append(res)

    tools_block = ""
    if tool_results:
        tools_block = "\n\nFerramentas utilizadas:\n" + "\n".join(
            f"- {r}" for r in tool_results
        )

    prompt = (
        f"SISTEMA:\n{system_msg}\n\n"
        f"USUÁRIO:\n{user_message}\n\n"
        f"{tools_block}\n\n"
        "ASSISTENTE: responda em português brasileiro, em poucos parágrafos."
    )

    try:
        response = model.generate_content(prompt)
        answer = response.text
    except Exception as e:
        answer = f"Erro ao gerar resposta: {e}"
    
    answer = apply_guardrails(answer)
    log_event("agent_answer", answer=answer)
    return answer