from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)

from app.core.dependencies import (
    get_current_user,
    get_resume_service,
)
from app.core.exceptions import ResumeNotFoundError
from app.models.user import User
from app.schemas.resume import (
    LatestResumeResponse,
    ResumeResponse,
)
from app.services.resume_service import ResumeService

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_resume(
    file: UploadFile = File(...),
    current_user: Annotated[User, Depends(get_current_user)] = None,
    resume_service: Annotated[
        ResumeService,
        Depends(get_resume_service),
    ] = None,
):
    resume = resume_service.upload_resume(
        file=file,
        current_user=current_user,
    )

    return ResumeResponse.model_validate(resume)


@router.get(
    "/latest",
    response_model=LatestResumeResponse,
)
def get_latest_resume(
    current_user: Annotated[User, Depends(get_current_user)],
    resume_service: Annotated[
        ResumeService,
        Depends(get_resume_service),
    ],
):
    """
    Returns the user's most recent resume with its parsed summary and skills.
    """
    resume = resume_service.get_latest_resume(current_user.id)

    if resume is None or resume.parsed_resume is None:
        raise ResumeNotFoundError(
            "No parsed resume found. Upload a resume first."
        )

    parsed = resume.parsed_resume

    return LatestResumeResponse(
        id=resume.id,
        filename=resume.filename,
        created_at=resume.created_at,
        summary=parsed.get("summary", ""),
        skills=parsed.get("skills", []),
    )
