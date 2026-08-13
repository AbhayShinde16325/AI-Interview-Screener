import json

from app.ai.prompts.interview_questions import (
    QUESTION_GENERATION_PROMPT,
)
from app.ai.resume_parser.schemas import ParsedResume


class PromptBuilder:
    """
    Builds the interview generation prompt.
    """

    def build(
        self,
        resume: ParsedResume,
        role: str,
        interview_plan: dict,
        knowledge_context: str,
    ) -> str:

        return QUESTION_GENERATION_PROMPT.format(
            role=role,
            resume=json.dumps(
                resume.model_dump(),
                indent=2,
            ),
            interview_plan=json.dumps(
                interview_plan,
                indent=2,
            ),
            knowledge_context=knowledge_context,
        )