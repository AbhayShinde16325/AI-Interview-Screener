import json

from pydantic import ValidationError

from app.ai.gemini.client import GeminiClient
from app.ai.prompts.resume_prompt import RESUME_ANALYSIS_PROMPT
from app.ai.resume_parser.schemas import ParsedResume


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
    ) -> ParsedResume:

        prompt = RESUME_ANALYSIS_PROMPT.format(
            resume_text=resume_text,
        )

        response = self.client.generate(prompt)
        
        
        try:
            response_json = json.loads(response)

        except json.JSONDecodeError:
            raise ValueError(
                "Gemini returned invalid JSON."
            )

        try:
            return ParsedResume.model_validate(
                response_json
            )

        except ValidationError as e:
            raise ValueError(
                f"Invalid resume schema: {e}"
            )