from pydantic import BaseModel, Field


class QuestionEvaluation(BaseModel):
    """Score + feedback for a single answered question."""

    question_order: int = Field(
        ge=1,
        description="Question order in the interview (1-based).",
    )
    score: int = Field(ge=0, le=10)
    feedback: str


class EvaluationResult(BaseModel):
    """Complete evaluation of an interview."""

    overall_score: int = Field(ge=0, le=100)
    recommendation: str
    strengths: list[str]
    improvements: list[str]
    summary: str
    question_evaluations: list[QuestionEvaluation]
