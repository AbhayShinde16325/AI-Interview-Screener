import json
import logging
import re

from pydantic import ValidationError

from app.ai.evaluation.schemas import EvaluationResult
from app.ai.gemini.client import GeminiClient
from app.ai.prompts.evaluation_prompt import EVALUATION_PROMPT

logger = logging.getLogger(__name__)


class Evaluator:
    """
    Evaluates a complete interview in a single Gemini request.
    """

    def __init__(self):
        self.client = GeminiClient()

    def evaluate(
        self,
        role: str,
        questions,
        max_retries: int = 1,
    ) -> EvaluationResult:
        payload = []

        for question in questions:
            item = {
                "question_order": question.question_order,
                "skill": question.skill,
                "difficulty": question.difficulty,
                "type": question.question_type,
                "question": question.question,
                "expected_topics": question.expected_topics,
                "candidate_answer": question.candidate_answer
                or "No answer provided",
            }

            # Give the evaluator the correct answer for MCQ questions so it
            # can grade them objectively.
            if question.question_type == "MCQ":
                item["options"] = question.options or []
                item["correct_answer"] = question.correct_answer or ""

            payload.append(item)

        prompt = EVALUATION_PROMPT.format(
            role=role,
            questions_json=json.dumps(payload, indent=2),
        )

        last_error: Exception | None = None

        for attempt in range(max_retries + 1):
            try:
                response = self.client.generate(prompt, temperature=0.3)
                data = self._parse_json(response)
                return EvaluationResult.model_validate(data)

            except (json.JSONDecodeError, ValidationError, ValueError) as exc:
                last_error = exc
                logger.warning(
                    "Evaluation attempt %d/%d failed: %s",
                    attempt + 1,
                    max_retries + 1,
                    exc,
                )

        raise ValueError(
            "Interview evaluation failed after "
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
