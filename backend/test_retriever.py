from app.ai.retrieval.retriever import Retriever

retriever = Retriever()

results = retriever.search(
    "Python decorators",
    k=3,
)

print("=" * 80)

for i, result in enumerate(results, start=1):

    print(f"Result {i}")

    print(
        "Distance:",
        result["distance"],
    )

    print(
        "Category:",
        result["metadata"]["category"],
    )

    print(
        "File:",
        result["metadata"]["filename"],
    )

    print(
        result["metadata"]["content"])

    print("-" * 80)