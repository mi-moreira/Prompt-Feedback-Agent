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

## Usage
- Chat tab: send a message, the agent may call tools (CEP lookup, Pokémon info) and cite Chroma context.
- Feedback & Prompt tab: rate answers and submit feedback to rewrite the system prompt; changes are stored in `data/prompt_state.json`.

## Testing MongoDB
With Mongo running and env set, you can validate connectivity:
```sh
python test_mongodb_connection.py
```

## Notes
- `.env` is ignored by git; keep secrets out of version control.
- Chroma data and prompt history are stored under `data/` locally.
- If you see Gemini quota/model errors, ensure the Generative Language API is enabled on a billed project and that `GEMINI_MODEL` matches an available model for your key.
