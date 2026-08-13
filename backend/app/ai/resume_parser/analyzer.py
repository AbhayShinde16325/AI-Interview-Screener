import json
import logging
import re

from pydantic import ValidationError

from app.ai.gemini.client import GeminiClient
from app.ai.prompts.resume_prompt import RESUME_ANALYSIS_PROMPT
from app.ai.resume_parser.schemas import ParsedResume

logger = logging.getLogger(__name__)


class ResumeAnalyzer:
    """
    Uses Gemini to analyze a resume and return
    a validated ParsedResume object.
    """

    def __init__(self):
        self.client = GeminiClient()

    def analyze(
        self,
        resume_text: str,
        max_retries: int = 1,
    ) -> ParsedResume:

        prompt = RESUME_ANALYSIS_PROMPT.format(
            resume_text=resume_text,
        )

        last_error: Exception | None = None

        for attempt in range(max_retries + 1):
            try:
                response = self.client.generate(prompt)
                response_json = self._parse_json(response)
                return ParsedResume.model_validate(response_json)

            except (json.JSONDecodeError, ValidationError, ValueError) as exc:
                last_error = exc
                logger.warning(
                    "Resume analysis attempt %d/%d failed: %s",
                    attempt + 1,
                    max_retries + 1,
                    exc,
                )

        raise ValueError(
            "Resume analysis failed after "
            f"{max_retries + 1} attempts: {last_error}"
        )

    @staticmethod
    def _parse_json(response: str) -> dict:
        """Parse Gemini output, tolerating ```json fences around the JSON."""
        response = response.strip()

        if response.startswith("```"):
            response = re.sub(r"^```(?:json)?\s*", "", response)
            response = re.sub(r"\s*```$", "", response)

        return json.loads(response)