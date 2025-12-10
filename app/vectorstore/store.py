from pathlib import Path
import chromadb

DATA_DIR = Path("data")
VECTOR_DIR = DATA_DIR / "chroma_db"
VECTOR_DIR.mkdir(exist_ok=True)

SEED_DOCS = [
    {
        "id": "1",
        "content": "A Morphia é uma plataforma de vendas com IA focada em tatuadores.",
    },
    {
        "id": "2",
        "content": "O agente auxilia com dúvidas sobre atendimento, vendas e organização de estúdios de tatuagem.",
    },
    {
        "id": "3",
        "content": "A Morphia integra IA com automação para fluxos de negócios em estúdios.",
    },
]

_client = None
_collection = None


def get_collection():
    global _client, _collection
    if _client is None:
        _client = chromadb.PersistentClient(path=str(VECTOR_DIR))
    if _collection is None:
        _collection = _client.get_or_create_collection("morphia_knowledge")
        if _collection.count() == 0:
            _collection.add(
                ids=[d["id"] for d in SEED_DOCS],
                documents=[d["content"] for d in SEED_DOCS],
            )
    return _collection


def retrieve_relevant_docs(query: str, k: int = 3) -> list[str]:
    col = get_collection()
    results = col.query(query_texts=[query], n_results=k)
    docs = results.get("documents", [[]])[0]
    return docs