from sqlalchemy.orm import Session

from app.models.interview import Interview
from app.models.interview_question import InterviewQuestion


class InterviewRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        interview: Interview,
    ) -> Interview:

        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)

        return interview

    def create_with_questions(
        self,
        interview: Interview,
        questions: list[InterviewQuestion],
    ) -> Interview:
        """
        Persist an interview and its questions in one atomic transaction.
        """
        self.db.add(interview)
        self.db.flush()  # assigns interview.id

        for question in questions:
            question.interview_id = interview.id

        self.db.add_all(questions)
        self.db.commit()
        self.db.refresh(interview)

        return interview

    def get_by_id(
        self,
        interview_id,
    ) -> Interview | None:

        return (
            self.db.query(Interview)
            .filter(Interview.id == interview_id)
            .first()
        )

    def get_by_id_and_user(
        self,
        interview_id,
        user_id,
    ) -> Interview | None:
        """
        Fetch an interview only if it belongs to the given user.
        Used to enforce ownership on every interview endpoint.
        """
        return (
            self.db.query(Interview)
            .filter(
                Interview.id == interview_id,
                Interview.user_id == user_id,
            )
            .first()
        )

    def list_by_user(
        self,
        user_id,
    ) -> list[Interview]:
        return (
            self.db.query(Interview)
            .filter(Interview.user_id == user_id)
            .order_by(Interview.started_at.desc())
            .all()
        )

    def update(
        self,
        interview: Interview,
    ) -> Interview:

        self.db.commit()
        self.db.refresh(interview)

        return interview
