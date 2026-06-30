from typing import Literal

from pydantic import BaseModel, Field


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
    ]

    question: str

    expected_topics: list[str]

    knowledge_source: str


class InterviewQuestionList(BaseModel):
    questions: list[InterviewQuestion]