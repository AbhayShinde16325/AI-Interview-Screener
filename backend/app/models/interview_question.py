import uuid

from sqlalchemy import ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class InterviewQuestion(Base):

    __tablename__ = "interview_questions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    interview_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interviews.id"),
        nullable=False,
    )

    question_order: Mapped[int] = mapped_column(
        Integer,
    )

    skill: Mapped[str] = mapped_column(
        String,
    )

    difficulty: Mapped[str] = mapped_column(
        String,
    )

    question_type: Mapped[str] = mapped_column(
        String,
    )

    question: Mapped[str] = mapped_column(
        Text,
    )

    expected_topics: Mapped[list] = mapped_column(
        JSON,
    )

    knowledge_source: Mapped[str] = mapped_column(
        String,
    )

    # MCQ-only fields (options + server-side correct answer)
    options: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    correct_answer: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    candidate_answer: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    interview = relationship(
        "Interview",
        back_populates="questions",
    )