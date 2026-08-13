import logging

from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.embeddings.faiss_store import FAISSStore
from app.ai.resume_parser.schemas import ParsedResume

logger = logging.getLogger(__name__)

INDEX_PATH = "knowledge_base/index/faiss.index"
METADATA_PATH = "knowledge_base/index/metadata.json"


class QueryBuilder:
    """Builds meaningful FAISS queries from a skill and the candidate resume.

    A bare skill name ("Python") retrieves generic chunks. Combining the
    skill with keywords from the candidate's own resume makes the query
    specific to the candidate while staying grounded in the knowledge base.
    """

    @staticmethod
    def for_skill(skill: str, resume: ParsedResume) -> str:
        skill_lower = skill.lower()

        mentions = [
            keyword
            for keyword in resume.keywords
            if skill_lower in keyword.lower()
            and keyword.lower() != skill_lower
        ]

        others = [
            keyword
            for keyword in resume.keywords
            if skill_lower not in keyword.lower()
        ]

        tokens = [skill] + mentions[:2] + others[:2]
        return " ".join(tokens)


class Retriever:
    """
    Retrieves the most relevant chunks from the knowledge base.

    The FAISS index is loaded lazily and cached at module level by
    ``get_retriever()`` so the embedding model + index are loaded only
    once per process, not once per request.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.store = FAISSStore()
        self._load_index()

    def _load_index(self) -> None:
        try:
            self.store.load(INDEX_PATH, METADATA_PATH)
            logger.info(
                "FAISS index loaded: %d chunks from %s",
                len(self.store.metadata),
                INDEX_PATH,
            )
        except Exception:
            logger.warning(
                "FAISS index not found at %s. Retrieval will return empty "
                "results until the index is built (scripts/build_index.py).",
                INDEX_PATH,
            )
            self.store.index = None
            self.store.metadata = []

    def search(self, query: str, k: int = 5) -> list[dict]:
        if self.store.index is None:
            return []

        embedding = self.embedding_service.embed(query)
        return self.store.search(embedding, k)


# ---------------------------------------------------------------------------
# Process-wide singleton
# ---------------------------------------------------------------------------
_retriever: "Retriever | None" = None


def get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever
