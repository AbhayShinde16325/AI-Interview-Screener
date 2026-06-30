from app.ai.embeddings.embedding_service import (
    EmbeddingService,
)
from app.ai.embeddings.faiss_store import (
    FAISSStore,
)


class Retriever:
    """
    Retrieves the most relevant chunks from
    the knowledge base.
    """

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.store = FAISSStore()

        self.store.load(
            "knowledge_base/index/faiss.index",
            "knowledge_base/index/metadata.json",
        )

    def search(
        self,
        query: str,
        k: int = 5,
    ) -> list[dict]:

        embedding = self.embedding_service.embed(
            query,
        )

        return self.store.search(
            embedding,
            k,
        )