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
from app.models.user import User
from app.schemas.resume import ResumeResponse
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
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ] = None,
    resume_service: Annotated[
        ResumeService,
        Depends(get_resume_service),
    ] = None,
):
    resume = resume_service.upload_resume(
        file=file,
        current_user=current_user,
    )

    return ResumeResponse.model_validate(
        resume
    )