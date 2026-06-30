from app.ai.retrieval.loader import (
    KnowledgeBaseLoader,
)

loader = KnowledgeBaseLoader()

documents = loader.load_documents()

print(f"Documents Loaded: {len(documents)}")

for doc in documents:
    print("-" * 60)
    print(doc["category"])
    print(doc["filename"])
    print(doc["content"][:200])