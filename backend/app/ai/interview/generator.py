import json
import logging
import re

from pydantic import ValidationError

from app.ai.gemini.client import GeminiClient
from app.ai.interview.normalizer import QuestionNormalizer
from app.ai.interview.prompt_builder import PromptBuilder
from app.ai.resume_parser.schemas import ParsedResume
from app.schemas.interview import InterviewQuestionList

logger = logging.getLogger(__name__)


class QuestionGenerator:
    """
    Generates the complete interview in a single Gemini request.
    """

    def __init__(self):
        self.client = GeminiClient()
        self.prompt_builder = PromptBuilder()

    def generate(
        self,
        resume: ParsedResume,
        role: str,
        interview_plan: dict,
        knowledge_context: str,
        max_retries: int = 1,
    ) -> InterviewQuestionList:
        prompt = self.prompt_builder.build(
            resume=resume,
            role=role,
            interview_plan=interview_plan,
            knowledge_context=knowledge_context,
        )

        last_error: Exception | None = None

        for attempt in range(max_retries + 1):
            try:
                response = self.client.generate(prompt)
                data = self._parse_json(response)
                data = QuestionNormalizer.normalize(data)
                result = InterviewQuestionList.model_validate(data)
                self._validate_count(result, interview_plan)
                return result

            except (json.JSONDecodeError, ValidationError, ValueError) as exc:
                last_error = exc
                logger.warning(
                    "Question generation attempt %d/%d failed: %s",
                    attempt + 1,
                    max_retries + 1,
                    exc,
                )

        raise ValueError(
            "Question generation failed after "
            f"{max_retries + 1} attempts: {last_error}"
        )

    @staticmethod
    def _parse_json(response: str) -> dict:
        """Parse Gemini output into the expected ``{"questions": [...]}`` shape.

        Tolerates ```json fences, and the case where Gemini returns the
        questions array directly instead of wrapping it in a top-level object.
        """
        response = response.strip()

        if response.startswith("```"):
            response = re.sub(r"^```(?:json)?\s*", "", response)
            response = re.sub(r"\s*```$", "", response)

        data = json.loads(response)

        if isinstance(data, list):
            data = {"questions": data}

        return data

    @staticmethod
    def _validate_count(
        result: InterviewQuestionList,
        interview_plan: dict,
    ) -> None:
        expected = interview_plan.get("total_questions")
        actual = len(result.questions)

        if expected is not None and actual != expected:
            logger.warning(
                "Interview plan requested %s questions but Gemini returned %s.",
                expected,
                actual,
            )
