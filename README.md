# Prompt Feedback Agent

Simple Streamlit app that chats with a Gemini model, pulls a few seeded facts from a Chroma vector store, and lets users submit feedback to iteratively improve the system prompt. MongoDB is included for persistence tests and future extensions.

## Stack
- Python 3.12, Streamlit
- Google Generative AI (Gemini)
- Chroma vector store (local persistent client)
- MongoDB (via Docker Compose for local use)

## Quickstart
1) Install dependencies
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2) Set environment variables (copy `.env.example` to `.env` and fill in)
- `GEMINI_API_KEY` (required)
- `GEMINI_MODEL` (optional, default: `models/gemini-pro-latest`)
- `MONGODB_URL`, `MONGODB_DATABASE` as needed

3) Start MongoDB (if you want local persistence/tests)
```sh
docker-compose up -d mongodb
```

4) Run the app
```sh
streamlit run ui/app.py
```

## Docker
- Build:
```sh
docker build -t morphia-chat .
```
- Run (make sure `.env` has your GEMINI_API_KEY/model; mount or use --env-file):
```sh
docker run --rm -p 8501:8501 --env-file .env morphia-chat
```
- MongoDB (optional) via compose:
```sh
docker-compose up -d mongodb
```
- To run app + Mongo via compose (no host Python): ensure `.env` uses the service host, e.g. `MONGODB_URL=mongodb://root:change-me@morphia-mongodb-local:27017/morphia_db?authSource=admin`, then:
```sh
docker-compose up --build
```

## External APIs
- ViaCEP (CEP lookup): mention a CEP (ex.: `CEP 01001000`) and the agent calls ViaCEP.
- PokéAPI (Pokémon info): mention a Pokémon name (ex.: `pokemon pikachu`) to fetch basic stats.

## API Documentation (used by the agent)
- ViaCEP: `https://viacep.com.br/ws/{CEP}/json/` (GET). Triggered when the user message contains a valid CEP pattern (8 digits). Errors: CEP inválido/não encontrado are handled in-code and surfaced to the user.
- PokéAPI: `https://pokeapi.co/api/v2/pokemon/{name}` (GET). Triggered when the user mentions “pokemon” + a name. Errors: Pokémon não encontrado handled in-code.

## Docs
- High-level overview: `docs/overview.md`

## Language / UX
- Default UX is Portuguese (PT-BR) for studio-facing users; docs are in English.
- UI labels can be toggled (PT/EN) in the app; system prompt/content remains PT-BR by default.
- Chroma is seeded with Morphia facts; prompt edits and history are stored locally in `data/prompt_state.json`.

## Usage
- Chat tab: send a message, the agent may call tools (CEP lookup, Pokémon info) and cite Chroma context.
- Feedback & Prompt tab: rate answers and submit feedback to rewrite the system prompt; changes are stored in `data/prompt_state.json`.

## Examples
- Contextual chat: “Me ajude a melhorar a descrição do meu estúdio de tatuagem.”
- CEP lookup (ViaCEP): “Qual o endereço do CEP 01001000?”
- PokéAPI: “pokemon pikachu” ou “Quais os tipos do pokemon charmander?”
- Feedback flow: após uma resposta, vá em “Feedback & Prompt”, dê uma nota e envie “Considere que cobro 1600 de sinal”; o prompt será atualizado e armazenado em `data/prompt_state.json`.

## Testing MongoDB
With Mongo running and env set, you can validate connectivity:
```sh
python test_mongodb_connection.py
```

## Notes
- `.env` is ignored by git; keep secrets out of version control.
- Chroma data and prompt history are stored under `data/` locally.
- If you see Gemini quota/model errors, ensure the Generative Language API is enabled on a billed project and that `GEMINI_MODEL` matches an available model for your key.
