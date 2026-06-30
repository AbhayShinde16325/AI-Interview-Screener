from uuid import UUID

from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        resume: Resume,
    ) -> Resume:
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)

        return resume

    def get_by_id(
        self,
        resume_id: UUID,
    ) -> Resume | None:
        return (
            self.db.query(Resume)
            .filter(Resume.id == resume_id)
            .first()
        )