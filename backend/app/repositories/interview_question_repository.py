from sqlalchemy.orm import Session

from app.models.interview_question import InterviewQuestion


class InterviewQuestionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        question: InterviewQuestion,
    ) -> InterviewQuestion:

        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)

        return question

    def create_many(
        self,
        questions: list[InterviewQuestion],
    ):

        self.db.add_all(questions)
        self.db.commit()

    def get_by_interview_id(
        self,
        interview_id,
    ) -> list[InterviewQuestion]:

        return (
            self.db.query(InterviewQuestion)
            .filter(InterviewQuestion.interview_id == interview_id)
            .order_by(InterviewQuestion.question_order)
            .all()
        )

    def get_by_id(
        self,
        question_id,
    ) -> InterviewQuestion | None:

        return (
            self.db.query(InterviewQuestion)
            .filter(InterviewQuestion.id == question_id)
            .first()
        )

    def update(
        self,
        question: InterviewQuestion,
    ) -> InterviewQuestion:

        self.db.commit()
        self.db.refresh(question)

        return question

    def commit_all(self) -> None:
        """Commit pending changes to all loaded questions (used by evaluation)."""
        self.db.commit()
