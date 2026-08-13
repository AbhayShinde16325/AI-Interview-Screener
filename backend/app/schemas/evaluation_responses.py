from uuid import UUID

from pydantic import BaseModel


class QuestionEvaluationResponse(BaseModel):
    question_order: int
    score: int
    feedback: str


class EvaluationResponse(BaseModel):
    interview_id: UUID
    status: str
    overall_score: int
    recommendation: str
    strengths: list[str]
    improvements: list[str]
    summary: str
    question_evaluations: list[QuestionEvaluationResponse]
