from google import genai
from google.genai import types

from app.core.config import settings


class GeminiClient:
    """
    Wrapper around the Google Gemini API.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

        # We will use Flash for the MVP.
        self.model = "gemini-2.5-flash"

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
    ) -> str:
        """
        Send a prompt to Gemini and return the generated text.
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
            ),
        )

        return response.text