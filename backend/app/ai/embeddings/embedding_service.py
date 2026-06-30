from google import genai

from app.core.config import settings


class EmbeddingService:
    """
    Generates embeddings using Google's embedding model.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

        self.model = "gemini-embedding-001"

    def embed(
        self,
        text: str,
    ) -> list[float]:

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
        )

        return response.embeddings[0].values