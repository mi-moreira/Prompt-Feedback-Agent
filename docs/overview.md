# Project Overview

Prompt Feedback Agent is a Streamlit app that chats with a Gemini model, grounds answers with a Chroma vector store, uses external tools (ViaCEP, PokéAPI), and lets users submit feedback to iteratively improve the system prompt. State (prompt and Chroma data) is persisted locally.

## Architecture at a glance
- UI (`ui/app.py`): Chat and Feedback tabs, language toggle (PT/EN labels), displays current prompt/history, quick prompts, tool hints.
- Agent (`app/agent/agent.py`): Builds system message with Chroma context, decides tool usage, calls LLM, applies guardrails, logs events.
- Tools (`app/agent/tools.py`): ViaCEP lookup, PokéAPI; triggered by simple keyword/regex.
- Vector store (`app/vectorstore/store.py`): Chroma PersistentClient storing seeded Morphia facts; queried per user message.
- Feedback loop (`app/feedback/feedback_engine.py`, `app/agent/prompts.py`): Generates a new system prompt from user feedback, saves prompt + history to `data/prompt_state.json`.
- Guardrails/Logging: basic redaction/length guard (`app/utils/guardrails.py`), structured logs (`app/utils/logging_utils.py`).

## Data & persistence
- Prompt state: `data/prompt_state.json` (ignored by git). Survives app restarts unless deleted.
- Chroma data: `data/chroma_db/` (ignored by git). Seeds are loaded on first run if collection is empty.
- MongoDB: optional; `docker-compose.yml` provides a Mongo service; `test_mongodb_connection.py` exercises basic CRUD.

## External services
- Gemini (Google Generative AI): model and API key via `GEMINI_API_KEY`/`GEMINI_MODEL`.
- ViaCEP: `https://viacep.com.br/ws/{CEP}/json/`
- PokéAPI: `https://pokeapi.co/api/v2/pokemon/{name}`

## Running
- Host: `streamlit run ui/app.py` (use localhost in `MONGODB_URL`).
- Docker: `docker build -t morphia-chat .` then `docker run --rm -p 8501:8501 --env-file .env morphia-chat`
- Compose (app + Mongo): `docker-compose up --build` with `MONGODB_URL` pointing to `mongodb` service (see README).
