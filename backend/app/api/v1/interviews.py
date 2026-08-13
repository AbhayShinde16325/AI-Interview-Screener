from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.mappers.interview_mapper import InterviewMapper
from app.models.user import User
from app.schemas.interview_requests import (
    StartInterviewRequest,
    SubmitAnswerRequest,
)
from app.schemas.interview_responses import (
    InterviewQuestionListResponse,
    InterviewListResponse,
    InterviewSummaryResponse,
    StartInterviewResponse,
    SubmitAnswerResponse,
)
from app.services.interview_service import InterviewService

router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"],
)


@router.post(
    "/start",
    response_model=StartInterviewResponse,
)
def start_interview(
    request: StartInterviewRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Creates a complete interview: resume → plan → RAG retrieval → questions.
    """
    service = InterviewService(db)

    interview = service.create_interview(
        current_user=current_user,
        role=request.role,
    )

    questions = service.get_questions(
        interview_id=interview.id,
        user_id=current_user.id,
    )

    return StartInterviewResponse(
        interview_id=interview.id,
        status=interview.status,
        role=interview.role,
        questions=InterviewMapper.to_question_list(questions),
    )


@router.get(
    "",
    response_model=InterviewListResponse,
)
def list_interviews(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Lists the current user's interviews (newest first).
    """
    service = InterviewService(db)

    interviews = service.list_interviews(current_user.id)

    return InterviewListResponse(
        interviews=[
            InterviewSummaryResponse(
                id=interview.id,
                role=interview.role,
                status=interview.status,
                score=interview.score,
                started_at=interview.started_at,
            )
            for interview in interviews
        ]
    )


@router.get(
    "/{interview_id}/questions",
    response_model=InterviewQuestionListResponse,
)
def get_questions(
    interview_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    service = InterviewService(db)

    interview, questions = service.get_interview_with_questions(
        interview_id=interview_id,
        user_id=current_user.id,
    )

    return InterviewQuestionListResponse(
        interview_id=interview_id,
        role=interview.role,
        questions=InterviewMapper.to_question_list(questions),
    )


@router.post(
    "/{interview_id}/answer",
    response_model=SubmitAnswerResponse,
)
def submit_answer(
    interview_id: UUID,
    request: SubmitAnswerRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    service = InterviewService(db)

    service.submit_answer(
        interview_id=interview_id,
        question_id=request.question_id,
        answer=request.answer,
        user_id=current_user.id,
    )

    return SubmitAnswerResponse(
        message="Answer submitted successfully.",
    )
