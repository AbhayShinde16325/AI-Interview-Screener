from app.ai.embeddings.embedding_service import (
    EmbeddingService,
)

service = EmbeddingService()

embedding = service.embed(
    """
    Python is an interpreted programming language.
    """
)

print(type(embedding))
print(len(embedding))

print(embedding[:10])