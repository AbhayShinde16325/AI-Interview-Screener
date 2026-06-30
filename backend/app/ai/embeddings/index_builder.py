from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.embeddings.faiss_store import FAISSStore
from app.ai.retrieval.chunker import DocumentChunker
from app.ai.retrieval.loader import KnowledgeBaseLoader


class IndexBuilder:
    """
    Builds the FAISS index from the knowledge base.
    """

    def __init__(self):
        self.loader = KnowledgeBaseLoader()
        self.chunker = DocumentChunker()
        self.embedding_service = EmbeddingService()
        self.store = FAISSStore()

    def build(self):

        documents = self.loader.load_documents()

        total_chunks = 0

        for document in documents:

            chunks = self.chunker.chunk(
                document["content"]
            )

            for chunk_number, chunk in enumerate(chunks):

                embedding = self.embedding_service.embed(
                    chunk
                )

                metadata = {
                    "category": document["category"],
                    "filename": document["filename"],
                    "chunk_number": chunk_number,
                    "content": chunk,
                }

                self.store.add(
                    embedding,
                    metadata,
                )

                total_chunks += 1

        self.store.save(
            "knowledge_base/index/faiss.index",
            "knowledge_base/index/metadata.json",
        )

        print("=" * 60)
        print("Index build completed.")
        print(f"Documents : {len(documents)}")
        print(f"Chunks    : {total_chunks}")
        print("=" * 60)