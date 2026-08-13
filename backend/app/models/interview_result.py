import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class InterviewResult(Base):

    __tablename__ = "interview_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    interview_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interviews.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    overall_score: Mapped[int] = mapped_column(
        Integer,
    )

    recommendation: Mapped[str] = mapped_column(
        Text,
    )

    strengths: Mapped[list] = mapped_column(
        JSON,
    )

    improvements: Mapped[list] = mapped_column(
        JSON,
    )

    summary: Mapped[str] = mapped_column(
        Text,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    interview = relationship(
        "Interview",
        back_populates="result",
    )
