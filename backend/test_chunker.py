from app.ai.retrieval.loader import KnowledgeBaseLoader
from app.ai.retrieval.chunker import DocumentChunker

loader = KnowledgeBaseLoader()
documents = loader.load_documents()

chunker = DocumentChunker(
    chunk_size=500,
    overlap=100,
)

for document in documents:

    chunks = chunker.chunk(
        document["content"]
    )

    print("=" * 80)

    print(
        f"{document['filename']} "
        f"({len(document['content'])} chars)"
    )

    print(f"Chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):

        print("-" * 80)
        print(f"Chunk {i}")
        print(f"Length: {len(chunk)}")
        print(chunk)