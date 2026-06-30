from app.ai.retrieval.context_builder import (
    ContextBuilder,
)

from app.ai.retrieval.retriever import (
    Retriever,
)

retriever = Retriever()

results = retriever.search(
    "Python decorators",
)

context = ContextBuilder().build(
    results,
)

print(context)