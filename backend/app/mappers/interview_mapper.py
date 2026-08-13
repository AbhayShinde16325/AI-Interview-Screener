from app.models.interview_question import InterviewQuestion

from app.schemas.interview_responses import (
    InterviewQuestionResponse,
)


class InterviewMapper:

    @staticmethod
    def to_question_response(
        question: InterviewQuestion,
    ) -> InterviewQuestionResponse:

        return InterviewQuestionResponse(
            id=question.id,
            question_order=question.question_order,
            skill=question.skill,
            difficulty=question.difficulty,
            question_type=question.question_type,
            question=question.question,
            expected_topics=question.expected_topics,
            knowledge_source=question.knowledge_source,
            options=question.options,
        )

    @staticmethod
    def to_question_list(
        questions: list[InterviewQuestion],
    ) -> list[InterviewQuestionResponse]:

        return [
            InterviewMapper.to_question_response(
                question,
            )
            for question in questions
        ]