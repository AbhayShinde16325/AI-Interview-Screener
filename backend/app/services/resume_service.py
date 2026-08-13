from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.ai.resume_parser.analyzer import ResumeAnalyzer
from app.core.config import settings
from app.core.exceptions import ValidationError
from app.models.resume import Resume
from app.models.user import User
from app.parsers.pdf_parser import PDFParser
from app.repositories.resume_repository import ResumeRepository

UPLOAD_DIRECTORY = Path(settings.upload_dir)
UPLOAD_DIRECTORY.mkdir(exist_ok=True)

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


class ResumeService:
    def __init__(self, db: Session):
        self.resume_repository = ResumeRepository(db)

    def upload_resume(
        self,
        file: UploadFile,
        current_user: User,
    ) -> Resume:
        # --- Validation ------------------------------------------------
        if file.content_type != "application/pdf":
            raise ValidationError("Only PDF files are allowed.")

        content = file.file.read()

        if not content:
            raise ValidationError("Uploaded file is empty.")

        if len(content) > MAX_FILE_SIZE_BYTES:
            raise ValidationError("File too large. Maximum size is 10 MB.")

        # --- Persist file ------------------------------------------------
        unique_filename = f"{uuid4()}.pdf"
        file_path = UPLOAD_DIRECTORY / unique_filename

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        # --- Extract + analyze --------------------------------------------
        extracted_text = PDFParser.extract_text(str(file_path))

        if not extracted_text.strip():
            raise ValidationError(
                "No extractable text found in the PDF. "
                "Make sure it is not a scanned image."
            )

        parsed_resume = ResumeAnalyzer().analyze(extracted_text)

        resume = Resume(
            user_id=current_user.id,
            filename=file.filename,
            file_path=str(file_path),
            extracted_text=extracted_text,
            parsed_resume=parsed_resume.model_dump(),
        )

        return self.resume_repository.create(resume)

    def get_latest_resume(
        self,
        user_id,
    ) -> Resume | None:
        return self.resume_repository.get_latest_by_user(user_id)
