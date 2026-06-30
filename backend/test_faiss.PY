from app.ai.embeddings.embedding_service import (
    EmbeddingService,
)

from app.ai.embeddings.faiss_store import (
    FAISSStore,
)

embedding_service = EmbeddingService()

store = FAISSStore()

texts = [
    "Python programming language",
    "FastAPI framework",
    "MongoDB database",
]

for text in texts:

    embedding = embedding_service.embed(
        text
    )

    store.add(
        embedding,
        {
            "text": text,
        },
    )

query = embedding_service.embed(
    "Python"
)

results = store.search(
    query,
    k=3,
)

print(results)