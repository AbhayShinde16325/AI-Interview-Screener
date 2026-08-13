from typing import Literal

from pydantic import BaseModel, model_validator


class InterviewQuestion(BaseModel):
    id: int

    skill: str

    difficulty: Literal[
        "Easy",
        "Medium",
        "Hard",
    ]

    type: Literal[
        "Conceptual",
        "Coding",
        "Scenario",
        "MCQ",
    ]

    question: str

    expected_topics: list[str]

    knowledge_source: str

    # MCQ-only fields (absent for written questions)
    options: list[str] | None = None
    correct_answer: str | None = None

    @model_validator(mode="after")
    def validate_mcq_fields(self):
        """MCQ questions must define options and a correct answer.

        ``correct_answer`` is persisted server-side and used for evaluation —
        it is never returned to the candidate.
        """
        if self.type == "MCQ":
            if not self.options or len(self.options) < 2:
                raise ValueError(
                    "MCQ questions must define at least 2 options."
                )
            if not self.correct_answer:
                raise ValueError(
                    "MCQ questions must define a correct_answer."
                )
        return self


class InterviewQuestionList(BaseModel):
    questions: list[InterviewQuestion]