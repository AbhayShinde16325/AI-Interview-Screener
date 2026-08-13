from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class InterviewQuestionResponse(BaseModel):

    id: UUID
    question_order: int
    skill: str
    difficulty: str
    question_type: str
    question: str
    expected_topics: list[str]
    knowledge_source: str
    # Candidate-facing options for MCQ questions (None for written ones).
    # Note: correct_answer is deliberately NOT exposed to the candidate.
    options: list[str] | None = None


class InterviewQuestionListResponse(BaseModel):

    interview_id: UUID
    role: str
    questions: list[InterviewQuestionResponse]


class StartInterviewResponse(BaseModel):

    interview_id: UUID
    status: str
    role: str
    questions: list[InterviewQuestionResponse]


class SubmitAnswerResponse(BaseModel):

    message: str


class InterviewSummaryResponse(BaseModel):

    id: UUID
    role: str
    status: str
    score: int | None = None
    started_at: datetime


class InterviewListResponse(BaseModel):

    interviews: list[InterviewSummaryResponse]
