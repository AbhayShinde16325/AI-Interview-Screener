from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.user import User
from app.repositories.resume_repository import ResumeRepository
from app.parsers.pdf_parser import PDFParser
from app.ai.resume_parser.analyzer import ResumeAnalyzer
UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)


class ResumeService:
    def __init__(
        self,
        db: Session,
    ):
        self.resume_repository = ResumeRepository(db)

    def upload_resume(
        self,
        file: UploadFile,
        current_user: User,
    ) -> Resume:

        # Validate content type
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed.",
            )

        # Generate unique filename
        unique_filename = (
            f"{uuid4()}.pdf"
        )

        file_path = (
            UPLOAD_DIRECTORY / unique_filename
        )

        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Extract text from the saved PDF
        extracted_text = PDFParser.extract_text(
            str(file_path)
        )
        
        parsed_resume = ResumeAnalyzer().analyze(
        extracted_text
        )
        resume = Resume(
            user_id=current_user.id,
            filename=file.filename,
            file_path=str(file_path),
            extracted_text=extracted_text,
            parsed_resume=parsed_resume.model_dump(),

        )
        
        return self.resume_repository.create(
            resume
        )