import json

from app.ai.gemini.client import GeminiClient
from app.ai.interview.normalizer import QuestionNormalizer
from app.ai.interview.prompt_builder import PromptBuilder
from app.ai.resume_parser.schemas import ParsedResume
from app.schemas.interview import InterviewQuestionList


class QuestionGenerator:
    """
    Generates interview questions using Gemini.
    """

    def __init__(self):
        self.client = GeminiClient()
        self.prompt_builder = PromptBuilder()

    def generate(
        self,
        resume: ParsedResume,
        skill: str,
        knowledge_context: str,
        question_count: int,
    ) -> InterviewQuestionList:

        prompt = self.prompt_builder.build(
            resume=resume,
            skill=skill,
            knowledge_context=knowledge_context,
            question_count=question_count,
        )

        response = self.client.generate(prompt)

        data = json.loads(response)

        data = QuestionNormalizer.normalize(data)

        return InterviewQuestionList.model_validate(data)