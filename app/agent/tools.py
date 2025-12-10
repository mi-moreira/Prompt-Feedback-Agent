import requests


class ToolError(Exception):
    pass


def lookup_cep(cep: str) -> dict:
    cep = cep.replace("-", "").strip()
    if len(cep) != 8 or not cep.isdigit():
        raise ToolError("CEP inválido. Use formato 00000000 ou 00000-000.")
    url = f"https://viacep.com.br/ws/{cep}/json/"
    resp = requests.get(url, timeout=5)
    if resp.status_code != 200:
        raise ToolError("Falha ao consultar ViaCEP.")
    data = resp.json()
    if "erro" in data:
        raise ToolError("CEP não encontrado.")
    return data


def get_pokemon(name: str) -> dict:
    name = name.lower().strip()
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    resp = requests.get(url, timeout=5)
    if resp.status_code != 200:
        raise ToolError("Pokémon não encontrado.")
    data = resp.json()
    return {
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "base_experience": data["base_experience"],
        "types": [t["type"]["name"] for t in data["types"]],
    }


TOOLS_REGISTRY = {
    "via_cep": {
        "description": "Consulta endereço pelo CEP brasileiro.",
        "func": lookup_cep,
    },
    "pokemon_info": {
        "description": "Obtém informações básicas de um Pokémon.",
        "func": get_pokemon,
    },
}