from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.evaluation_responses import (
    EvaluationResponse,
    QuestionEvaluationResponse,
)
from app.services.interview_service import InterviewService

router = APIRouter(
    prefix="/interviews",
    tags=["Evaluation"],
)


def _to_response(result, interview) -> EvaluationResponse:
    """Build the response from the stored result + per-question scores."""
    return EvaluationResponse(
        interview_id=interview.id,
        status=interview.status,
        overall_score=result.overall_score,
        recommendation=result.recommendation,
        strengths=result.strengths,
        improvements=result.improvements,
        summary=result.summary,
        question_evaluations=[
            QuestionEvaluationResponse(
                question_order=question.question_order,
                score=question.score,
                feedback=question.feedback,
            )
            for question in sorted(
                interview.questions,
                key=lambda q: q.question_order,
            )
        ],
    )


@router.post(
    "/{interview_id}/complete",
    response_model=EvaluationResponse,
)
def complete_interview(
    interview_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Evaluates all answered questions and returns the interview result.
    """
    service = InterviewService(db)
    result, interview = service.complete_interview(
        interview_id=interview_id,
        user_id=current_user.id,
    )
    return _to_response(result, interview)


@router.get(
    "/{interview_id}/result",
    response_model=EvaluationResponse,
)
def get_result(
    interview_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Returns the stored evaluation for a completed interview.
    """
    service = InterviewService(db)
    interview = service._get_owned_interview(interview_id, current_user.id)
    result = service.get_interview_result(
        interview_id=interview_id,
        user_id=current_user.id,
    )
    return _to_response(result, interview)
